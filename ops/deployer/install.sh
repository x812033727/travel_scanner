#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run this installer as root." >&2
  exit 1
fi

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AGENT_TARGET="/opt/travel-scanner-deployer/deployment_agent"
install -d -m 0750 /opt/travel-scanner-deployer /etc/travel-scanner
install -d -m 0750 /srv/travel-scanner/releases /var/backups/travel-scanner
install -d -m 0750 /var/lib/travel-scanner-deployer /run/travel-scanner-deployer

getent group travel-api >/dev/null || groupadd --system --gid 10002 travel-api
id travel-deployer >/dev/null 2>&1 || useradd --system --create-home --home-dir /var/lib/travel-scanner-deployer --shell /usr/sbin/nologin travel-deployer
usermod -aG docker travel-deployer

if [[ "${AGENT_TARGET}" != "/opt/travel-scanner-deployer/deployment_agent" ]]; then
  echo "Refusing to replace an unexpected agent path." >&2
  exit 1
fi
rm -rf -- "${AGENT_TARGET}"
cp -a "${SOURCE_ROOT}/apps/api/deployment_agent" /opt/travel-scanner-deployer/
chown -R root:travel-deployer /opt/travel-scanner-deployer
chown -R travel-deployer:travel-deployer /srv/travel-scanner /var/backups/travel-scanner /var/lib/travel-scanner-deployer
chown travel-deployer:travel-api /run/travel-scanner-deployer

install -m 0644 "${SOURCE_ROOT}/ops/deployer/travel-scanner-deployer.service" /etc/systemd/system/
if [[ ! -f /etc/travel-scanner/deployer.env ]]; then
  install -m 0640 -o root -g travel-deployer "${SOURCE_ROOT}/ops/deployer/deployer.env.example" /etc/travel-scanner/deployer.env
fi
systemctl daemon-reload
echo "Edit /etc/travel-scanner/deployer.env, then run: systemctl enable --now travel-scanner-deployer"
