#!/usr/bin/env bash
# Install or upgrade the AI accounts agent on the production host. Safe to re-run.
#
#   bash ops/ai-accounts/install.sh [--runtime-env /root/travel_scanner/.env]
#
# The first run moves root's existing Claude Code and Codex logins into account A and
# leaves /root/.claude, /root/.claude.json and /root/.codex as links to it, so anything
# that runs the CLIs without the shell functions keeps using the same account.
set -euo pipefail
# The host's default umask once made deployed files unreadable (2026-09-07); be explicit.
umask 022

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run this installer as root." >&2
  exit 1
fi

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HERE="${SOURCE_ROOT}/ops/ai-accounts"
STATE=/var/lib/mokaair-ai-accounts
OPT=/opt/mokaair-ai-accounts
LIB=/usr/local/lib/mokaair-ai-accounts
ENV_FILE=/etc/travel-scanner/ai-accounts.env
SLOTS=(a b c d e)
# What a new account shares with account A: instructions, agents, skills and plugins, and
# the session history, so `--resume` works whichever account a session started on.
CLAUDE_SHARED=(CLAUDE.md agents commands skills plugins output-styles projects)
CODEX_SHARED=(AGENTS.md prompts skills sessions)
RUNTIME_ENV=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --runtime-env)
      RUNTIME_ENV="${2:?--runtime-env needs a path}"
      shift 2
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

cli_running() {
  local link target
  for link in /proc/[0-9]*/exe; do
    target="$(readlink "${link}" 2>/dev/null || true)"
    case "${target}" in
      /root/.local/share/claude/versions/* | *codex-linux-*) return 0 ;;
    esac
  done
  return 1
}

needs_move() {
  [[ -e "$1" && ! -L "$1" ]]
}

# 1. Accounts and state.
getent group travel-api >/dev/null || groupadd --system --gid 10002 travel-api
install -d -m 0700 "${STATE}" "${STATE}/home"
for slot in "${SLOTS[@]}"; do
  install -d -m 0700 "${STATE}/claude-${slot}" "${STATE}/codex-${slot}"
done

# 2. First run: move the existing logins into account A.
if needs_move /root/.claude || needs_move /root/.claude.json || needs_move /root/.codex; then
  if cli_running; then
    echo "A claude or codex process is running. Close every session, then run this again." >&2
    exit 3
  fi
fi
move_into_slot() {
  local legacy="$1" slot="$2"
  if needs_move "${legacy}"; then
    if [[ -n "$(ls -A "${slot}")" ]]; then
      echo "${slot} is not empty; leaving ${legacy} where it is." >&2
      return 1
    fi
    rmdir "${slot}"
    mv "${legacy}" "${slot}"
    echo "Moved ${legacy} into ${slot}."
  fi
  [[ -e "${legacy}" || -L "${legacy}" ]] || ln -s "${slot}" "${legacy}"
}
move_into_slot /root/.claude "${STATE}/claude-a"
move_into_slot /root/.codex "${STATE}/codex-a"
if needs_move /root/.claude.json; then
  if [[ -e "${STATE}/claude-a/.claude.json" ]]; then
    echo "${STATE}/claude-a/.claude.json exists; leaving /root/.claude.json where it is." >&2
  else
    mv /root/.claude.json "${STATE}/claude-a/.claude.json"
    echo "Moved /root/.claude.json into ${STATE}/claude-a."
  fi
fi
[[ -e /root/.claude.json || -L /root/.claude.json ]] ||
  ln -s "${STATE}/claude-a/.claude.json" /root/.claude.json
chmod 0700 "${STATE}/claude-a" "${STATE}/codex-a"

# 3. Accounts B-E share A's instructions and history and start from its settings.
share_with_a() {
  local tool="$1" name="$2" slot
  [[ -e "${STATE}/${tool}-a/${name}" ]] || return 0
  for slot in "${SLOTS[@]:1}"; do
    [[ -e "${STATE}/${tool}-${slot}/${name}" || -L "${STATE}/${tool}-${slot}/${name}" ]] ||
      ln -s "../${tool}-a/${name}" "${STATE}/${tool}-${slot}/${name}"
  done
}
copy_from_a() {
  local tool="$1" name="$2" slot
  [[ -f "${STATE}/${tool}-a/${name}" ]] || return 0
  for slot in "${SLOTS[@]:1}"; do
    [[ -e "${STATE}/${tool}-${slot}/${name}" ]] ||
      install -m 0600 "${STATE}/${tool}-a/${name}" "${STATE}/${tool}-${slot}/${name}"
  done
}
for name in "${CLAUDE_SHARED[@]}"; do share_with_a claude "${name}"; done
for name in "${CODEX_SHARED[@]}"; do share_with_a codex "${name}"; done
# The agent points each account's status line at its own recorder when it starts.
copy_from_a claude settings.json
copy_from_a claude mokaair-statusline-chain.json
copy_from_a codex config.toml
# MCP servers live in .claude.json next to the login; give new accounts the same servers.
if [[ -f "${STATE}/claude-a/.claude.json" ]]; then
  for slot in "${SLOTS[@]:1}"; do
    target="${STATE}/claude-${slot}/.claude.json"
    [[ -e "${target}" ]] && continue
    python3 - "${STATE}/claude-a/.claude.json" "${target}" <<'PY'
import json, os, sys
source, target = sys.argv[1], sys.argv[2]
try:
    servers = json.load(open(source, encoding="utf-8")).get("mcpServers")
except (OSError, ValueError, AttributeError):
    servers = None
if servers:
    descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        json.dump({"mcpServers": servers}, handle, indent=2)
PY
  done
fi
for tool in claude codex; do
  [[ -f "${STATE}/default-${tool}" ]] || printf 'a\n' >"${STATE}/default-${tool}"
  chmod 0600 "${STATE}/default-${tool}"
done

# 4. The agent, the status line recorder and the account commands.
install -d -m 0755 "${OPT}" "${LIB}"
rm -rf -- "${OPT}/ai_accounts_agent"
cp -a "${SOURCE_ROOT}/apps/api/ai_accounts_agent" "${OPT}/"
find "${OPT}" -name __pycache__ -prune -exec rm -rf {} +
chown -R root:root "${OPT}"
chmod -R u=rwX,go=rX "${OPT}"
install -m 0755 "${HERE}/statusline-record" "${LIB}/statusline-record"
install -m 0755 "${HERE}/mokaair-ai-cli" "${LIB}/mokaair-ai-cli"
for slot in "${SLOTS[@]}"; do
  ln -sfn "${LIB}/mokaair-ai-cli" "/usr/local/bin/claude-${slot}"
  ln -sfn "${LIB}/mokaair-ai-cli" "/usr/local/bin/codex-${slot}"
done
install -m 0644 "${HERE}/profile.sh" /etc/profile.d/mokaair-ai-accounts.sh
# tmux windows and other non-login shells read only ~/.bashrc.
grep -q 'mokaair-ai-accounts' /root/.bashrc 2>/dev/null ||
  printf '\n[ -r /etc/profile.d/mokaair-ai-accounts.sh ] && . /etc/profile.d/mokaair-ai-accounts.sh  # mokaair-ai-accounts\n' \
    >>/root/.bashrc

# 5. The key the API signs with. Never printed: an install run from an agent session
#    would otherwise leave it in a transcript.
[[ -d /etc/travel-scanner ]] || install -d -m 0750 /etc/travel-scanner
if [[ ! -f "${ENV_FILE}" ]]; then
  (
    umask 077
    printf 'AI_ACCOUNTS_AGENT_HMAC_KEY=%s\n# Comma-separated; a login that ends on any other account is signed out again.\nAI_ACCOUNTS_ALLOWED_EMAILS=\n' \
      "$(python3 -c 'import secrets; print(secrets.token_hex(32))')" >"${ENV_FILE}"
  )
  echo "Created ${ENV_FILE} with a new AI_ACCOUNTS_AGENT_HMAC_KEY."
fi
chown root:root "${ENV_FILE}"
chmod 0600 "${ENV_FILE}"
if [[ -n "${RUNTIME_ENV}" ]]; then
  key_line="$(grep '^AI_ACCOUNTS_AGENT_HMAC_KEY=' "${ENV_FILE}")"
  if grep -q '^AI_ACCOUNTS_AGENT_HMAC_KEY=' "${RUNTIME_ENV}"; then
    python3 - "${RUNTIME_ENV}" "${key_line}" <<'PY'
import os, sys
path, line = sys.argv[1], sys.argv[2]
text = open(path, encoding="utf-8").read().splitlines()
text = [line if row.startswith("AI_ACCOUNTS_AGENT_HMAC_KEY=") else row for row in text]
mode = os.stat(path).st_mode & 0o777
with open(path, "w", encoding="utf-8") as handle:
    handle.write("\n".join(text) + "\n")
os.chmod(path, mode)
PY
  else
    printf '%s\n' "${key_line}" >>"${RUNTIME_ENV}"
  fi
  grep -q '^AI_ACCOUNTS_ENABLED=' "${RUNTIME_ENV}" ||
    printf 'AI_ACCOUNTS_ENABLED=true\n' >>"${RUNTIME_ENV}"
  echo "AI_ACCOUNTS_AGENT_HMAC_KEY and AI_ACCOUNTS_ENABLED are in ${RUNTIME_ENV} (values not printed)."
fi

# 6. The service. Enabling it stays a separate, deliberate step.
install -m 0644 "${HERE}/mokaair-ai-accounts.service" /etc/systemd/system/mokaair-ai-accounts.service
systemctl daemon-reload
if systemctl is-active --quiet mokaair-ai-accounts; then
  systemctl restart mokaair-ai-accounts
  echo "Restarted mokaair-ai-accounts."
else
  echo "Next: add the owner's emails to AI_ACCOUNTS_ALLOWED_EMAILS in ${ENV_FILE}, then run"
  echo "  systemctl enable --now mokaair-ai-accounts"
fi
