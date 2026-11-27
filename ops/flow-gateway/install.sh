#!/usr/bin/env bash
# Install or upgrade the Mokaair Flow & Flow Music MCP gateway on the production host.
# Safe to re-run.
#
#   bash ops/flow-gateway/install.sh [--runtime-env /root/travel_scanner/.env]
set -euo pipefail
umask 022

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run this installer as root." >&2
  exit 1
fi

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HERE="${SOURCE_ROOT}/ops/flow-gateway"
OPT="/opt/mokaair-flow-gateway/travel_scanner"
ENV_FILE="/etc/travel-scanner/flow-gateway.env"
SOCKET_DIR="/run/mokaair-flow-gateway"
SOCKET_PATH="${SOCKET_DIR}/gateway.sock"
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

# 1. Accounts, group, runtime directories.
getent group travel-api >/dev/null || groupadd --system --gid 10002 travel-api
id flowbot >/dev/null 2>&1 || useradd --create-home --shell /bin/bash flowbot
install -d -m 0750 -o flowbot -g travel-api "${SOCKET_DIR}"
install -d -m 0750 -o flowbot -g flowbot /home/flowbot/logs /home/flowbot/.mokaair-flow /home/flowbot/.mokaair-flow-music

# 2. Sync gateway code (zero npm dependencies, pure Node 22+ ESM under tools/video/).
install -d -m 0755 "${OPT}/tools"
rm -rf -- "${OPT}/tools/video"
cp -a "${SOURCE_ROOT}/tools/video" "${OPT}/tools/video"
install -m 0644 "${SOURCE_ROOT}/package.json" "${OPT}/package.json"
chown -R root:root /opt/mokaair-flow-gateway
chmod -R u=rwX,go=rX /opt/mokaair-flow-gateway
# Keep episode/music workspaces and Drive rule cache writable by non-root flowbot across upgrades.
install -d -m 0750 -o flowbot -g flowbot \
  "${OPT}/work" \
  "${OPT}/work/video-episodes" \
  "${OPT}/work/music-library" \
  "${OPT}/.cache" \
  "${OPT}/.cache/video-drive"
chown -R flowbot:flowbot "${OPT}/work" "${OPT}/.cache"

# 3. Shared HMAC secret (never printed to stdout).
install -d -m 0755 /etc/travel-scanner
if [[ ! -f "${ENV_FILE}" ]]; then
  (
    umask 077
    cat >"${ENV_FILE}" <<EOF
FLOW_MCP_GATEWAY_SECRET=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
MOKAAIR_FLOW_HOME=/home/flowbot/.mokaair-flow
MOKAAIR_FLOW_MUSIC_HOME=/home/flowbot/.mokaair-flow-music
EOF
  )
  echo "Created ${ENV_FILE} with a new FLOW_MCP_GATEWAY_SECRET."
fi
chown flowbot:flowbot "${ENV_FILE}"
chmod 0600 "${ENV_FILE}"

# 4. Wire API runtime .env (preserving permissions, never printing secret).
if [[ -n "${RUNTIME_ENV}" ]]; then
  if [[ -s "${RUNTIME_ENV}" && -n "$(tail -c1 "${RUNTIME_ENV}")" ]]; then
    printf '\n' >>"${RUNTIME_ENV}"
  fi
  secret_line="$(grep '^FLOW_MCP_GATEWAY_SECRET=' "${ENV_FILE}")"
  python3 - "${RUNTIME_ENV}" "${secret_line}" "${SOCKET_PATH}" <<'PY'
import os, sys
path, secret_line, socket_path = sys.argv[1], sys.argv[2], sys.argv[3]
updates = {
    "FLOW_MCP_GATEWAY_ENABLED": "FLOW_MCP_GATEWAY_ENABLED=true",
    "FLOW_MCP_GATEWAY_SOCKET": f"FLOW_MCP_GATEWAY_SOCKET={socket_path}",
    "FLOW_MCP_GATEWAY_SECRET": secret_line,
}
lines = open(path, encoding="utf-8").read().splitlines()
seen = set()
out = []
for row in lines:
    key = row.split("=", 1)[0] if "=" in row else ""
    if key in updates:
        out.append(updates[key])
        seen.add(key)
    else:
        out.append(row)
for key, value in updates.items():
    if key not in seen:
        out.append(value)
mode = os.stat(path).st_mode & 0o777
with open(path, "w", encoding="utf-8") as handle:
    handle.write("\n".join(out) + "\n")
os.chmod(path, mode)
PY
  echo "Updated FLOW_MCP_GATEWAY_* in ${RUNTIME_ENV} (values not printed)."
fi

# 5. Install and enable systemd service.
install -m 0644 "${HERE}/mokaair-flow-gateway.service" /etc/systemd/system/mokaair-flow-gateway.service
systemctl daemon-reload
systemctl enable --now mokaair-flow-gateway
systemctl restart mokaair-flow-gateway
systemctl is-active mokaair-flow-gateway
ls -la "${SOCKET_PATH}"
