#!/usr/bin/env bash
# Make a fresh shell (a Claude Code cloud session, a Codex sandbox, a laptop) able to run
# MiniMax H3 on Colab:
#
#   bootstrap.sh            install + token + verify
#   bootstrap.sh install    the Colab CLI (pinned) and the upstream skill (pinned commit)
#   bootstrap.sh token      write the CLI token: from the site (a video tool token with Colab
#                           access fetches the account signed in on /admin/ai-accounts), or
#                           from the COLAB_CLI_TOKEN_JSON secret
#   bootstrap.sh verify     prove the pairing: `colab usage` must print the balance (exit 4 if not)
#   bootstrap.sh patch      re-apply the sampling profile to the upstream notebook (H3_PROFILE:
#                           smooth (default) | hero | draft; H3_NOTEBOOK_PATCH=off leaves upstream's)
#                           and the 1920x1088 canvas cap to the notebook and the upstream runner
#
# Idempotent: re-running changes nothing that is already right. Nothing here needs sudo.
# The upstream repository has no licence file, so it is not vendored: it is cloned at a
# pinned commit into MINIMAX_H3_COLAB_HOME (default: ~/.cache/minimax-h3-colab-skill).
# The cloud environment's setup script cannot read secrets, so `token` runs inside the
# session, where the environment variables exist. Contains no credentials.
#
# Where the token comes from, in order:
#   1. COLAB_CLI_TOKEN_JSON              the token.json itself (raw or base64), an environment secret
#   2. the site, through the video tool token the session paired with
#      (`node tools/video/cli.mjs login --colab`, allowed on the admin card): MOKAAIR_VIDEO_TOKEN
#      or ~/.mokaair/video-tool.json, and MOKAAIR_SITE (default https://mokaair.com);
#      COLAB_ACCOUNT_SLOT picks the account (a-e, default: the admin's default Colab account)
#   3. a token already at ~/.config/colab-cli/token.json
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
  # The notebook may carry our sampling patch: restore upstream's bytes before moving or re-patching.
  git -C "$SKILL_HOME" checkout --quiet -- . 2>/dev/null || true
  if [[ "$head" != "$UPSTREAM_COMMIT" ]]; then
    git -C "$SKILL_HOME" fetch --quiet origin "$UPSTREAM_COMMIT" || git -C "$SKILL_HOME" fetch --quiet origin
    git -C "$SKILL_HOME" checkout --quiet "$UPSTREAM_COMMIT"
  fi
  for required in SKILL.md scripts/runner.py assets/MiniMax_H3_Turbo_Colab.ipynb; do
    [[ -f "$SKILL_HOME/$required" ]] || die "upstream checkout is missing $required" 2
  done
  say "upstream skill at $SKILL_HOME @ ${UPSTREAM_COMMIT:0:12}"
  patch_notebook
}

patch_notebook() {
  # Upstream samples Ref2VA with the 4-step turbo LoRA (references barely apply) and both modes
  # with euler + beta; the patch swaps in the 8-step LoRAs (profile `smooth`) or the base-model
  # settings (`hero`), and for every profile raises the 1344x768 canvas cap in the notebook and
  # in scripts/runner.py to 1920x1088 (proven on an A100 2026-10-28). Exact-string edits on the
  # pristine files; see scripts/patch_notebook.py.
  if [[ "${H3_NOTEBOOK_PATCH:-on}" == "off" ]]; then
    say "notebook patch off (H3_NOTEBOOK_PATCH=off): upstream's 4-step Ref2VA / drbaph FL2VA settings and 1344x768 cap"
    return
  fi
  [[ -f "$SKILL_HOME/assets/MiniMax_H3_Turbo_Colab.ipynb" ]] || die "no notebook to patch; run: bootstrap.sh install" 2
  git -C "$SKILL_HOME" checkout --quiet -- assets/ scripts/runner.py 2>/dev/null || true
  MINIMAX_H3_COLAB_HOME="$SKILL_HOME" python3 -I "$(dirname "$0")/patch_notebook.py" || die "the sampling profile could not be applied (see above)" "$?"
}

site_token() {
  # The video tool token: the environment, or the file `node tools/video/cli.mjs login` wrote.
  if [[ -n "${MOKAAIR_VIDEO_TOKEN:-}" ]]; then
    printf '%s' "$MOKAAIR_VIDEO_TOKEN"
    return
  fi
  local file="${MOKAAIR_VIDEO_TOOL_FILE:-$HOME/.mokaair/video-tool.json}"
  [[ -s "$file" ]] || return 1
  python3 -I -c 'import json, sys
data = json.load(open(sys.argv[1], encoding="utf-8"))
token = data.get("token")
print(token) if isinstance(token, str) and token.startswith("mkv_") else sys.exit(1)' "$file"
}

site_url() {
  if [[ -n "${MOKAAIR_SITE:-}" ]]; then
    printf '%s' "${MOKAAIR_SITE%/}"
    return
  fi
  local file="${MOKAAIR_VIDEO_TOOL_FILE:-$HOME/.mokaair/video-tool.json}"
  if [[ -s "$file" ]]; then
    python3 -I -c 'import json, sys
site = json.load(open(sys.argv[1], encoding="utf-8")).get("site")
print(site.rstrip("/")) if isinstance(site, str) and site.startswith("https://") else sys.exit(1)' "$file" && return
  fi
  printf 'https://mokaair.com'
}

fetch_from_site() {
  # Prints the token.json the site hands a paired session, or returns 1 with the reason on stderr.
  local token site slot url body status
  token="$(site_token)" || return 1
  site="$(site_url)"
  slot="${COLAB_ACCOUNT_SLOT:-default}"
  [[ "$slot" =~ ^([a-e]|default)$ ]] || die "COLAB_ACCOUNT_SLOT must be a-e or default" 2
  url="$site/api/video/colab-credentials?slot=$slot"
  body="$(curl -sS -m 30 -H "Authorization: Bearer $token" -H "Accept: application/json" -w '\n%{http_code}' "$url")" || { say "cannot reach $site" >&2; return 1; }
  status="${body##*$'\n'}"
  body="${body%$'\n'*}"
  if [[ "$status" != "200" ]]; then
    say "the site refused the Colab credentials (HTTP $status): $(printf '%s' "$body" | python3 -I -c 'import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get("code") or "", data.get("detail") or "")
except ValueError:
    print("not JSON")')" >&2
    return 1
  fi
  printf '%s' "$body" | python3 -I -c 'import json, sys
data = json.load(sys.stdin)
credentials = data.get("credentials")
if not isinstance(credentials, dict) or not credentials.get("refresh_token"):
    sys.exit("the site answered without a usable token")
print("[minimax-h3-colab] account slot " + str(data.get("slot")), file=sys.stderr)
print(json.dumps(credentials))'
}

write_token() {
  local secret="${COLAB_CLI_TOKEN_JSON:-}"
  local source="COLAB_CLI_TOKEN_JSON"
  if [[ -z "$secret" ]]; then
    if secret="$(fetch_from_site)"; then
      source="the site (video tool token with Colab access)"
    elif [[ -s "$TOKEN_PATH" ]]; then
      say "no COLAB_CLI_TOKEN_JSON and no site pairing in this shell; keeping the token already at $TOKEN_PATH"
      return
    else
      say "no token source: pair with the site (node tools/video/cli.mjs login --colab, then allow it on the admin card), set COLAB_CLI_TOKEN_JSON, or run scripts/pair.py start"
      return
    fi
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
  say "token written to $TOKEN_PATH from $source"
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
  patch) patch_notebook ;;
  all) install_cli; install_upstream; write_token; verify ;;
  -h|--help) sed -n '2,17p' "$0" ;;
  *) die "unknown step: $step (install | token | verify | patch | all)" 2 ;;
esac
