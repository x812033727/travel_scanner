#!/usr/bin/env bash
# Make a fresh shell (a Claude Code cloud session, a Codex sandbox, a laptop) able to run
# MiniMax H3 on Colab:
#
#   bootstrap.sh            install + token + verify
#   bootstrap.sh install    the Colab CLI (pinned) and the upstream skill (pinned commit)
#   bootstrap.sh token      write the CLI token from the COLAB_CLI_TOKEN_JSON secret, if set
#   bootstrap.sh verify     prove the pairing: `colab usage` must print the balance (exit 4 if not)
#
# Idempotent: re-running changes nothing that is already right. Nothing here needs sudo.
# The upstream repository has no licence file, so it is not vendored: it is cloned at a
# pinned commit into MINIMAX_H3_COLAB_HOME (default: ~/.cache/minimax-h3-colab-skill).
# The cloud environment's setup script cannot read secrets, so `token` runs inside the
# session, where the environment variable exists. Contains no credentials.
set -Eeuo pipefail

UPSTREAM_REPO="${MINIMAX_H3_UPSTREAM_REPO:-https://github.com/killkli/minimax-h3-colab-skill.git}"
UPSTREAM_COMMIT="${MINIMAX_H3_UPSTREAM_COMMIT:-0a0d3b9c0060c97aeb4e13b1516c83d42939a304}"
COLAB_CLI_VERSION="${COLAB_CLI_VERSION:-0.7.5}"
SKILL_HOME="${MINIMAX_H3_COLAB_HOME:-$HOME/.cache/minimax-h3-colab-skill}"
CONFIG_DIR="${COLAB_CLI_CONFIG_DIR:-$HOME/.config/colab-cli}"
TOKEN_PATH="$CONFIG_DIR/token.json"
export PATH="$HOME/.local/bin:$PATH"

say() { printf '[minimax-h3-colab] %s\n' "$*"; }
die() { printf '[minimax-h3-colab] %s\n' "$1" >&2; exit "${2:-1}"; }

python_ok() {
  python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)' 2>/dev/null
}

install_cli() {
  if command -v colab >/dev/null 2>&1 && colab version 2>/dev/null | grep -q "$COLAB_CLI_VERSION"; then
    say "colab CLI $COLAB_CLI_VERSION already installed"
    return
  fi
  command -v uv >/dev/null 2>&1 || die "uv is missing; install it first (https://docs.astral.sh/uv/) or put a colab CLI $COLAB_CLI_VERSION on PATH" 2
  if python_ok; then
    uv tool install --quiet "google-colab-cli==$COLAB_CLI_VERSION"
  else
    uv tool install --quiet --python 3.12 "google-colab-cli==$COLAB_CLI_VERSION"
  fi
  command -v colab >/dev/null 2>&1 || die "colab is still not on PATH; add \$HOME/.local/bin to PATH" 2
  say "installed colab CLI $(colab version 2>/dev/null | tr -d '\n')"
}

install_upstream() {
  if [[ ! -d "$SKILL_HOME/.git" ]]; then
    mkdir -p "$(dirname "$SKILL_HOME")"
    git clone --quiet "$UPSTREAM_REPO" "$SKILL_HOME"
  fi
  local head
  head="$(git -C "$SKILL_HOME" rev-parse HEAD 2>/dev/null || true)"
  if [[ "$head" != "$UPSTREAM_COMMIT" ]]; then
    git -C "$SKILL_HOME" fetch --quiet origin "$UPSTREAM_COMMIT" || git -C "$SKILL_HOME" fetch --quiet origin
    git -C "$SKILL_HOME" checkout --quiet "$UPSTREAM_COMMIT"
  fi
  for required in SKILL.md scripts/runner.py assets/MiniMax_H3_Turbo_Colab.ipynb; do
    [[ -f "$SKILL_HOME/$required" ]] || die "upstream checkout is missing $required" 2
  done
  say "upstream skill at $SKILL_HOME @ ${UPSTREAM_COMMIT:0:12}"
}

write_token() {
  local secret="${COLAB_CLI_TOKEN_JSON:-}"
  if [[ -z "$secret" ]]; then
    if [[ -s "$TOKEN_PATH" ]]; then
      say "no COLAB_CLI_TOKEN_JSON in this shell; keeping the token already at $TOKEN_PATH"
      return
    fi
    say "no COLAB_CLI_TOKEN_JSON and no token at $TOKEN_PATH: pair first with scripts/pair.py start"
    return
  fi
  local decoded
  if [[ "$secret" == \{* ]]; then
    decoded="$secret"
  else
    decoded="$(printf '%s' "$secret" | tr -d '[:space:]' | base64 -d 2>/dev/null)" || die "COLAB_CLI_TOKEN_JSON is neither JSON nor base64 of JSON" 3
  fi
  printf '%s' "$decoded" | python3 -I -c 'import json, sys
data = json.load(sys.stdin)
missing = [k for k in ("refresh_token", "client_id", "client_secret") if not data.get(k)]
sys.exit("COLAB_CLI_TOKEN_JSON lacks " + ", ".join(missing) if missing else 0)' || die "COLAB_CLI_TOKEN_JSON is not a usable token (pair again and export it)" 3
  mkdir -p "$CONFIG_DIR"
  chmod 700 "$CONFIG_DIR"
  local tmp
  tmp="$(mktemp "$CONFIG_DIR/.token.XXXXXX")"
  printf '%s\n' "$decoded" > "$tmp"
  chmod 600 "$tmp"
  mv -f "$tmp" "$TOKEN_PATH"
  say "token written to $TOKEN_PATH from COLAB_CLI_TOKEN_JSON"
}

verify() {
  command -v colab >/dev/null 2>&1 || die "colab is not on PATH; run: bootstrap.sh install" 2
  local output
  output="$(timeout 90 colab --auth=oauth2 usage </dev/null 2>&1 || true)"
  if printf '%s' "$output" | grep -q "Current balance"; then
    printf '%s\n' "$output" | grep -E "Current balance|Usage rate|Active assignments"
    say "paired: the Colab CLI reads the account's compute units"
    return
  fi
  if printf '%s' "$output" | grep -q "accounts.google.com/o/oauth2"; then
    die "not paired: the CLI asked for a Google sign-in. Run scripts/pair.py start, or set COLAB_CLI_TOKEN_JSON and run: bootstrap.sh token" 4
  fi
  printf '%s\n' "$output" | tail -n 8 >&2
  die "colab usage neither printed a balance nor asked to sign in (network, proxy or revoked token?)" 4
}

step="${1:-all}"
case "$step" in
  install) install_cli; install_upstream ;;
  token) write_token ;;
  verify) verify ;;
  all) install_cli; install_upstream; write_token; verify ;;
  -h|--help) sed -n '2,15p' "$0" ;;
  *) die "unknown step: $step (install | token | verify | all)" 2 ;;
esac
