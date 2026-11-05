#!/usr/bin/env bash
# Pod start: the gate answers at once (port 8188, what the broker opens), the models are fetched
# or verified on the network volume, and only then ComfyUI starts behind the gate on 127.0.0.1.
set -euo pipefail

COMFY_DIR="${COMFY_DIR:-/opt/ComfyUI}"
MODELS_DIR="${MODELS_DIR:-/workspace/models}"
STATUS_FILE="${GATE_STATUS_FILE:-/tmp/gate-status.json}"
export GATE_STATUS_FILE="$STATUS_FILE"

python3 /opt/gate/gate.py &
gate=$!
trap 'kill "$gate" 2>/dev/null || true' EXIT

if ! python3 /opt/gate/fetch_models.py --lock /opt/gate/models.lock --dest "$MODELS_DIR" --status "$STATUS_FILE"; then
  # The gate stays up so the runner can read why; the broker's reaper stops the pod.
  wait "$gate"
  exit 1
fi

rm -rf "$COMFY_DIR/models"
ln -s "$MODELS_DIR" "$COMFY_DIR/models"
cd "$COMFY_DIR"
python3 main.py --listen 127.0.0.1 --port 8189 --disable-auto-launch &
comfy=$!
wait -n "$gate" "$comfy"
