#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run this installer as root." >&2
  exit 1
fi

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
AGENT_TARGET="/opt/travel-scanner-deployer/deployment_agent"

# Accounts first, so that the ownership applied below can reference them.
getent group travel-api >/dev/null || groupadd --system --gid 10002 travel-api
id travel-deployer >/dev/null 2>&1 || useradd --system --create-home --home-dir /var/lib/travel-scanner-deployer --shell /usr/sbin/nologin travel-deployer
# Membership in the docker group is root-equivalent on this host; see README.md.
usermod -aG docker travel-deployer

install -d -m 0750 /opt/travel-scanner-deployer /etc/travel-scanner
install -d -m 0750 /srv/travel-scanner/releases /var/backups/travel-scanner
install -d -m 0750 /var/lib/travel-scanner-deployer /run/travel-scanner-deployer

rm -rf -- "${AGENT_TARGET}"
cp -a "${SOURCE_ROOT}/apps/api/deployment_agent" /opt/travel-scanner-deployer/
chown -R root:travel-deployer /opt/travel-scanner-deployer
chown -R travel-deployer:travel-deployer /srv/travel-scanner /var/backups/travel-scanner /var/lib/travel-scanner-deployer
# The agent must traverse /etc/travel-scanner to hand runtime.env to docker compose, and the
# API container (gid travel-api) must traverse the socket directory. Both are re-asserted on
# every run because /run is recreated on reboot and earlier installs left them root-only.
chown root:travel-deployer /etc/travel-scanner
chmod 0750 /etc/travel-scanner
chown travel-deployer:travel-api /run/travel-scanner-deployer
chmod 0750 /run/travel-scanner-deployer

install -m 0644 "${SOURCE_ROOT}/ops/deployer/travel-scanner-deployer.service" /etc/systemd/system/
if [[ ! -f /etc/travel-scanner/deployer.env ]]; then
  install -m 0640 -o root -g travel-deployer "${SOURCE_ROOT}/ops/deployer/deployer.env.example" /etc/travel-scanner/deployer.env
fi
# Secret files stay root-owned and readable only by the agent group, even when they pre-exist.
chown root:travel-deployer /etc/travel-scanner/deployer.env
chmod 0640 /etc/travel-scanner/deployer.env
if [[ -f /etc/travel-scanner/runtime.env ]]; then
  chown root:travel-deployer /etc/travel-scanner/runtime.env
  chmod 0640 /etc/travel-scanner/runtime.env
else
  echo "Create /etc/travel-scanner/runtime.env (root:travel-deployer, mode 0640) before starting the agent." >&2
fi
systemctl daemon-reload
echo "Edit /etc/travel-scanner/deployer.env, then run: systemctl enable --now travel-scanner-deployer"
