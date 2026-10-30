#!/usr/bin/env bash
# Run the upstream runner from wherever bootstrap.sh put it, with this skill's defaults:
#
#   h3.sh usage                              compute units left (free; proves the pairing)
#   h3.sh check --manifest jobs.json         offline manifest check (scripts/check_manifest.py); free
#   h3.sh single --image a.png --prompt p.txt --mode first_frame --output out.mp4
#   h3.sh batch --manifest jobs.json --output-dir out/ --progress out/progress.json
#   h3.sh start --session NAME | h3.sh stop --session NAME
#   h3.sh test                               upstream's offline tests (fake colab, no credits)
#   h3.sh images-check --manifest ff.json    offline first-frame manifest check (check_images_manifest.py)
#   h3.sh images --manifest ff.json --output-dir first-frames/ [--session NAME] [--progress p.json]
#                                            paint first frames with Qwen-Image-Edit (scripts/images.py);
#                                            runs the check first (--no-check skips it)
#   h3.sh refine --manifest r.json --output-dir out/ [--session NAME]
#                                            stage 2: upscale a draft clip and re-denoise its low-noise
#                                            tail at 1312x736 (scripts/refine.py, references/three-stage.md)
#   h3.sh upscale --input-dir in/ --output-dir out/ [--model 7b|3b] [--session NAME]
#                                            stage 3: SeedVR2 to exactly 1920x1080 (scripts/upscale.py)
#
# Every other argument goes to scripts/runner.py of the upstream skill unchanged; on a single-shape
# GPU (COLAB_GPU or --gpu G4 or L4) batch, single and start also get --no-high-mem, because Colab
# rejects G4 with a high-RAM shape.
# Defaults (override with the environment): COLAB_GPU=A100, COLAB_EXEC_TIMEOUT=3600,
# COLAB_AUTH=oauth2, MINIMAX_H3_COLAB_HOME=~/.cache/minimax-h3-colab-skill.
# `batch` runs the manifest check first and stops on errors (--no-check skips it). `single
# --mode first_frame` without --width/--height uses H3_FIRST_FRAME_SIZE (default 1312x736: within
# 0.005 of 16:9, so a 16:9 keyframe is not stretched the way the 1344x768 canvas stretches it).
set -Eeuo pipefail

SKILL_HOME="${MINIMAX_H3_COLAB_HOME:-$HOME/.cache/minimax-h3-colab-skill}"
RUNNER="$SKILL_HOME/scripts/runner.py"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$HOME/.local/bin:$PATH"
export COLAB_AUTH="${COLAB_AUTH:-oauth2}"
export COLAB_GPU="${COLAB_GPU:-A100}"
export COLAB_EXEC_TIMEOUT="${COLAB_EXEC_TIMEOUT:-3600}"

case "${1:-}" in
  "" | -h | --help) sed -n '2,25p' "$0"; exit 0 ;;
  check)
    shift
    manifest=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --manifest) manifest="${2:-}"; shift 2 ;;
        --manifest=*) manifest="${1#--manifest=}"; shift ;;
        *) manifest="${manifest:-$1}"; shift ;;
      esac
    done
    [[ -n "$manifest" ]] || { echo "[minimax-h3-colab] check needs --manifest <jobs.json>" >&2; exit 2; }
    exec python3 -I "$HERE/check_manifest.py" "$manifest" ;;
  images-check)
    shift
    manifest=""
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --manifest) manifest="${2:-}"; shift 2 ;;
        --manifest=*) manifest="${1#--manifest=}"; shift ;;
        *) manifest="${manifest:-$1}"; shift ;;
      esac
    done
    [[ -n "$manifest" ]] || { echo "[minimax-h3-colab] images-check needs --manifest <ff.json>" >&2; exit 2; }
    exec python3 -I "$HERE/check_images_manifest.py" "$manifest" ;;
  images)
    # This skill's own runner and notebook: no upstream runner needed, only the colab CLI.
    shift
    args=(); manifest=""; check=1
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --no-check) check=0; shift ;;
        --manifest) manifest="${2:-}"; args+=("$1" "${2:-}"); shift 2 ;;
        --manifest=*) manifest="${1#--manifest=}"; args+=("$1"); shift ;;
        *) args+=("$1"); shift ;;
      esac
    done
    [[ -n "$manifest" ]] || { echo "[minimax-h3-colab] images needs --manifest <ff.json>" >&2; exit 2; }
    if [[ $check -eq 1 ]]; then
      python3 -I "$HERE/check_images_manifest.py" "$manifest" || { echo "[minimax-h3-colab] fix the manifest or pass --no-check" >&2; exit 1; }
    fi
    exec python3 -I "$HERE/images.py" batch "${args[@]}" ;;
  refine)
    shift
    exec python3 -I "$HERE/refine.py" "$@" ;;
  upscale)
    shift
    exec python3 -I "$HERE/upscale.py" "$@" ;;
esac

# --no-high-mem for a single-shape GPU, unless the caller already chose either way.
single_shape_flag() {
  local gpu="$COLAB_GPU" arg prev=""
  for arg in "$@"; do
    case "$arg" in
      --high-mem|--no-high-mem) return 0 ;;
      --gpu=*) gpu="${arg#--gpu=}" ;;
    esac
    [[ "$prev" == "--gpu" ]] && gpu="$arg"
    prev="$arg"
  done
  case "${gpu^^}" in G4|L4) printf '%s' "--no-high-mem" ;; esac
}

[[ -f "$RUNNER" ]] || { echo "[minimax-h3-colab] upstream runner missing at $RUNNER; run bootstrap.sh install" >&2; exit 2; }

case "$1" in
  test) cd "$SKILL_HOME" && exec python3 -m unittest discover -s tests -v ;;
  usage) shift; exec python3 "$RUNNER" usage --json "$@" ;;
  batch)
    shift
    args=(); manifest=""; check=1
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --no-check) check=0; shift ;;
        --manifest) manifest="${2:-}"; args+=("$1" "${2:-}"); shift 2 ;;
        --manifest=*) manifest="${1#--manifest=}"; args+=("$1"); shift ;;
        *) args+=("$1"); shift ;;
      esac
    done
    if [[ $check -eq 1 && -n "$manifest" ]]; then
      python3 -I "$HERE/check_manifest.py" "$manifest" || { echo "[minimax-h3-colab] fix the manifest or pass --no-check" >&2; exit 1; }
    fi
    flag="$(single_shape_flag "${args[@]}")"
    exec python3 "$RUNNER" batch "${args[@]}" ${flag:+"$flag"} ;;
  single)
    shift
    args=(); mode=""; sized=0
    for arg in "$@"; do
      case "$arg" in
        --width|--height|--width=*|--height=*) sized=1 ;;
      esac
    done
    while [[ $# -gt 0 ]]; do
      case "$1" in
        --mode) mode="${2:-}"; args+=("$1" "${2:-}"); shift 2 ;;
        --mode=*) mode="${1#--mode=}"; args+=("$1"); shift ;;
        *) args+=("$1"); shift ;;
      esac
    done
    if [[ "$mode" == "first_frame" && $sized -eq 0 ]]; then
      size="${H3_FIRST_FRAME_SIZE:-1312x736}"
      [[ "$size" =~ ^([0-9]+)x([0-9]+)$ ]] || { echo "[minimax-h3-colab] H3_FIRST_FRAME_SIZE must look like 1312x736" >&2; exit 2; }
      args+=(--width "${BASH_REMATCH[1]}" --height "${BASH_REMATCH[2]}")
    fi
    flag="$(single_shape_flag "${args[@]}")"
    exec python3 "$RUNNER" single "${args[@]}" ${flag:+"$flag"} ;;
  start)
    shift
    flag="$(single_shape_flag "$@")"
    exec python3 "$RUNNER" start "$@" ${flag:+"$flag"} ;;
  *) exec python3 "$RUNNER" "$@" ;;
esac
