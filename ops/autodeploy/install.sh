#!/usr/bin/env bash
# Install or upgrade the auto deploy timer on the production host. Run as root from a
# reviewed checkout: sudo bash ops/autodeploy/install.sh
#
# Copies the module and the verify script to /opt/travel-scanner-autodeploy (a deploy must
# not change the poller underneath itself, so it does not run from the checkout), installs
# the systemd units, creates the state directory and the env file from the example when it
# is missing, and does NOT enable the timer: that is the last step of the rollout task
# (tasks/open/2026-10-07-autodeploy-rollout-and-skill-docs.md), with the owner present.
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run this installer as root." >&2
  exit 1
fi

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TARGET=/opt/travel-scanner-autodeploy
ENV_FILE=/etc/travel-scanner/autodeploy.env

install -d -m 0750 "${TARGET}" /var/lib/travel-scanner-autodeploy
install -d -m 0750 /etc/travel-scanner
install -m 0644 "${SOURCE_ROOT}/ops/autodeploy/autodeploy.py" "${TARGET}/autodeploy.py"
install -m 0644 "${SOURCE_ROOT}/ops/autodeploy/README.md" "${TARGET}/README.md"
# The post-deploy verification the deploy skill runs by hand; the poller fills EXPECTED_SHA in.
install -m 0644 "${SOURCE_ROOT}/.agents/skills/deploy/scripts/host-verify.sh" "${TARGET}/host-verify.sh"
install -m 0644 "${SOURCE_ROOT}/ops/autodeploy/travel-scanner-autodeploy.service" /etc/systemd/system/
install -m 0644 "${SOURCE_ROOT}/ops/autodeploy/travel-scanner-autodeploy.timer" /etc/systemd/system/
if [[ ! -f "${ENV_FILE}" ]]; then
  install -m 0600 -o root -g root "${SOURCE_ROOT}/ops/autodeploy/autodeploy.env.example" "${ENV_FILE}"
fi
# The env file holds the GitHub token: root only, even when it pre-exists.
chown root:root "${ENV_FILE}"
chmod 0600 "${ENV_FILE}"
systemctl daemon-reload

python3 - <<'PY'
import sys
if sys.version_info < (3, 11):
    sys.exit(f"python3 is {sys.version.split()[0]}; the poller needs 3.11 or newer")
PY
if ! command -v flock >/dev/null; then
  echo "flock (util-linux) is missing; the poller probes the deploy lock with it" >&2
  exit 1
fi

cat <<MSG
Installed to ${TARGET}.
Next:
  1. Edit ${ENV_FILE}: set AUTODEPLOY_GITHUB_TOKEN; keep AUTODEPLOY_ENABLED=false.
  2. python3 ${TARGET}/autodeploy.py tick --dry-run     # one decision line per gate
  3. systemctl enable --now travel-scanner-autodeploy.timer   # still dry-run while ENABLED=false
  4. After a week of correct decisions: AUTODEPLOY_ENABLED=true (no restart needed; each tick reads the file).
MSG
