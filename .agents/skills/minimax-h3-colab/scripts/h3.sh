#!/usr/bin/env bash
# Run the upstream runner from wherever bootstrap.sh put it, with this skill's defaults:
#
#   h3.sh usage                              compute units left (free; proves the pairing)
#   h3.sh check --manifest jobs.json         offline manifest check (scripts/check_manifest.py); free
#   h3.sh single --image a.png --prompt p.txt --mode first_frame --output out.mp4
#   h3.sh batch --manifest jobs.json --output-dir out/ --progress out/progress.json
#   h3.sh start --session NAME | h3.sh stop --session NAME
#   h3.sh test                               upstream's offline tests (fake colab, no credits)
#
# Every other argument goes to scripts/runner.py of the upstream skill unchanged.
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
  "" | -h | --help) sed -n '2,17p' "$0"; exit 0 ;;
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
esac

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
    exec python3 "$RUNNER" batch "${args[@]}" ;;
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
    exec python3 "$RUNNER" single "${args[@]}" ;;
  *) exec python3 "$RUNNER" "$@" ;;
esac
