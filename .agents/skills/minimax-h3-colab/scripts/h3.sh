#!/usr/bin/env bash
# Run the upstream runner from wherever bootstrap.sh put it, with this skill's defaults:
#
#   h3.sh usage                              compute units left (free; proves the pairing)
#   h3.sh single --image a.png --prompt p.txt --mode first_frame --output out.mp4
#   h3.sh batch --manifest jobs.json --output-dir out/ --progress out/progress.json
#   h3.sh start --session NAME | h3.sh stop --session NAME
#   h3.sh test                               upstream's offline tests (fake colab, no credits)
#
# Every other argument goes to scripts/runner.py of the upstream skill unchanged.
# Defaults (override with the environment): COLAB_GPU=A100, COLAB_EXEC_TIMEOUT=3600,
# COLAB_AUTH=oauth2, MINIMAX_H3_COLAB_HOME=~/.cache/minimax-h3-colab-skill.
set -Eeuo pipefail

SKILL_HOME="${MINIMAX_H3_COLAB_HOME:-$HOME/.cache/minimax-h3-colab-skill}"
RUNNER="$SKILL_HOME/scripts/runner.py"
export PATH="$HOME/.local/bin:$PATH"
export COLAB_AUTH="${COLAB_AUTH:-oauth2}"
export COLAB_GPU="${COLAB_GPU:-A100}"
export COLAB_EXEC_TIMEOUT="${COLAB_EXEC_TIMEOUT:-3600}"

[[ -f "$RUNNER" ]] || { echo "[minimax-h3-colab] upstream runner missing at $RUNNER; run bootstrap.sh install" >&2; exit 2; }

case "${1:-}" in
  "" | -h | --help) sed -n '2,12p' "$0"; exit 0 ;;
  test) cd "$SKILL_HOME" && exec python3 -m unittest discover -s tests -v ;;
  usage) shift; exec python3 "$RUNNER" usage --json "$@" ;;
  *) exec python3 "$RUNNER" "$@" ;;
esac
