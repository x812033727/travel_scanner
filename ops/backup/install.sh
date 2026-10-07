#!/usr/bin/env bash
# Install or upgrade the nightly backup on the production host. Run as root from a reviewed
# checkout: sudo bash ops/backup/install.sh
#
# Copies the module, the manifest path list and the README to /opt/travel-scanner-backup,
# installs the systemd units, creates the run and state directories and the env file from the
# example when it is missing, and does NOT enable the timer: run `backup.py run --dry-run` and
# one real `run` by hand first (README.md).
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run this installer as root." >&2
  exit 1
fi

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TARGET=/opt/travel-scanner-backup
ENV_FILE=/etc/travel-scanner/backup.env

install -d -m 0750 "${TARGET}" /var/lib/travel-scanner-backup
install -d -m 0750 /etc/travel-scanner
# /var/backups/travel-scanner belongs to the deployment agent's installer (travel-deployer);
# nightly/ underneath is root's and must not be readable by anyone else.
install -d -m 0750 /var/backups/travel-scanner
install -d -m 0700 /var/backups/travel-scanner/nightly
install -m 0644 "${SOURCE_ROOT}/ops/backup/backup.py" "${TARGET}/backup.py"
install -m 0644 "${SOURCE_ROOT}/ops/backup/manifest-paths.txt" "${TARGET}/manifest-paths.txt"
install -m 0644 "${SOURCE_ROOT}/ops/backup/README.md" "${TARGET}/README.md"
install -m 0644 "${SOURCE_ROOT}/ops/backup/travel-scanner-backup.service" /etc/systemd/system/
install -m 0644 "${SOURCE_ROOT}/ops/backup/travel-scanner-backup.timer" /etc/systemd/system/
if [[ ! -f "${ENV_FILE}" ]]; then
  install -m 0600 -o root -g root "${SOURCE_ROOT}/ops/backup/backup.env.example" "${ENV_FILE}"
fi
chown root:root "${ENV_FILE}"
chmod 0600 "${ENV_FILE}"
systemctl daemon-reload

python3 - <<'PY'
import sys
if sys.version_info < (3, 11):
    sys.exit(f"python3 is {sys.version.split()[0]}; the backup needs 3.11 or newer")
PY
for tool in flock age; do
  if ! command -v "$tool" >/dev/null; then
    echo "NOTE: $tool is not installed (apt install age / util-linux); the run needs it" >&2
  fi
done

cat <<MSG
Installed to ${TARGET}.
Next:
  1. Edit ${ENV_FILE}: set BACKUP_AGE_RECIPIENT (the identity stays in the password manager).
  2. python3 ${TARGET}/backup.py run --dry-run
  3. python3 ${TARGET}/backup.py run          # one real run by hand, then check the directory
  4. systemctl enable --now travel-scanner-backup.timer
MSG
