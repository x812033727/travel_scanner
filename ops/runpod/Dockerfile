# MiniMax H3 on a RunPod pod: ComfyUI behind a bearer-token gate, models on the network volume.
# Everything that decides what runs is pinned here; the models are pinned in models.lock.
# Built and published by .github/workflows/runpod-h3-image.yml; ops/runpod/README.md has the rest.
FROM python:3.12-slim-bookworm@sha256:e697c81897302a4c4333bade000d98038fbb21eb064f8ee1fd42d02ebcd9d337 AS image

ENV COMFYUI_COMMIT=b5a432157de6b8884f81104cd02926adf4d597e4 \
    VHS_COMMIT=4d907bee61e92c2e65af3bd6383a4e4d356126d1 \
    SEEDVR2_COMMIT=4490bd1f482e026674543386bb2a4d176da245b9 \
    COMFY_DIR=/opt/ComfyUI \
    MODELS_DIR=/workspace/models \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl ffmpeg git libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# CUDA 13 with the INT8 ConvRot weights, the pair the Colab notebook picks. FP8 on CUDA 12.8 took
# 31.7 s a step on the same card (2026-10-31), against about 5 s on Colab.
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cu130 \
    torch==2.9.1+cu130 torchvision==0.24.1+cu130 torchaudio==2.9.1+cu130

RUN git init -q "$COMFY_DIR" \
    && git -C "$COMFY_DIR" fetch -q --depth 1 https://github.com/Comfy-Org/ComfyUI.git "$COMFYUI_COMMIT" \
    && git -C "$COMFY_DIR" checkout -q FETCH_HEAD \
    && mkdir -p "$COMFY_DIR/custom_nodes/ComfyUI-VideoHelperSuite" "$COMFY_DIR/custom_nodes/ComfyUI-SeedVR2_VideoUpscaler" \
    && git -C "$COMFY_DIR/custom_nodes/ComfyUI-VideoHelperSuite" init -q \
    && git -C "$COMFY_DIR/custom_nodes/ComfyUI-VideoHelperSuite" fetch -q --depth 1 https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git "$VHS_COMMIT" \
    && git -C "$COMFY_DIR/custom_nodes/ComfyUI-VideoHelperSuite" checkout -q FETCH_HEAD \
    && git -C "$COMFY_DIR/custom_nodes/ComfyUI-SeedVR2_VideoUpscaler" init -q \
    && git -C "$COMFY_DIR/custom_nodes/ComfyUI-SeedVR2_VideoUpscaler" fetch -q --depth 1 https://github.com/numz/ComfyUI-SeedVR2_VideoUpscaler.git "$SEEDVR2_COMMIT" \
    && git -C "$COMFY_DIR/custom_nodes/ComfyUI-SeedVR2_VideoUpscaler" checkout -q FETCH_HEAD \
    && grep -vE '^torch(vision|audio)?([<>=].*)?$' "$COMFY_DIR/requirements.txt" > /tmp/comfy.txt \
    && grep -vE '^(torch|torchvision)$' "$COMFY_DIR/custom_nodes/ComfyUI-SeedVR2_VideoUpscaler/requirements.txt" > /tmp/seedvr.txt \
    && pip install --no-cache-dir -r /tmp/comfy.txt -r "$COMFY_DIR/custom_nodes/ComfyUI-VideoHelperSuite/requirements.txt" -r /tmp/seedvr.txt \
    && rm /tmp/comfy.txt /tmp/seedvr.txt

COPY ops/runpod/gate.py ops/runpod/fetch_models.py ops/runpod/models.lock ops/runpod/entrypoint.sh ops/runpod/smoke.py /opt/gate/
COPY ops/runpod/workflows /opt/gate/workflows
RUN chmod +x /opt/gate/entrypoint.sh

LABEL org.opencontainers.image.source="https://github.com/x812033727/travel_scanner"
EXPOSE 8188
ENTRYPOINT ["/opt/gate/entrypoint.sh"]

# CI only (--target smoke): ComfyUI starts on CPU with no models and has every workflow node.
FROM image AS smoke
RUN cd "$COMFY_DIR" \
    && (python3 main.py --cpu --listen 127.0.0.1 --port 8189 --disable-auto-launch > /tmp/comfy.log 2>&1 &) \
    && for _ in $(seq 1 60); do curl -fsS -o /dev/null http://127.0.0.1:8189/system_stats && break; sleep 5; done \
    && tail -n 40 /tmp/comfy.log \
    && python3 /opt/gate/smoke.py
