#!/usr/bin/env bash
# Wrapper for runpod_runner.py: usage, check, single, batch, images, refine, upscale, start, stop.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${PYTHON:-python3}" -I "$here/runpod_runner.py" "$@"
