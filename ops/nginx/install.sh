#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run this installer as root." >&2
  exit 1
fi

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONF_D="/etc/nginx/conf.d"
SNIPPETS="/etc/nginx/snippets"
SITE_TARGET="/etc/nginx/sites-available/mokaair.conf"

if [[ ! -d /etc/nginx ]]; then
  echo "No /etc/nginx on this host; install nginx before running this." >&2
  exit 1
fi

install -d -m 0755 "${CONF_D}" "${SNIPPETS}"

# Re-applied on every run, like the rest of this repo's host installers: these two are ours
# outright, so overwriting them is how an upgrade reaches the host at all.
install -m 0644 "${SOURCE_ROOT}/10-rate-limit.conf" "${CONF_D}/mokaair-rate-limit.conf"
install -m 0644 "${SOURCE_ROOT}/proxy-headers.conf" "${SNIPPETS}/mokaair-proxy-headers.conf"

# The site file is the operator's: it carries server_name and certificate paths this repo
# does not know. Seed it once, then leave it alone -- overwriting it on an upgrade would
# replace a working certificate path with a placeholder and take the site down on reload.
if [[ ! -f "${SITE_TARGET}" ]]; then
  install -d -m 0755 /etc/nginx/sites-available
  install -m 0644 "${SOURCE_ROOT}/mokaair.conf.example" "${SITE_TARGET}"
  echo "Seeded ${SITE_TARGET}. Edit every line marked EDIT before enabling it."
else
  echo "Kept existing ${SITE_TARGET}; compare it against mokaair.conf.example by hand."
fi

# Deliberately no reload. A bad config that nginx accepts at -t can still be wrong for this
# host, and reloading from inside an installer removes the operator's chance to look first.
cat <<'NEXT'

Next, in this order:
  1. Edit /etc/nginx/sites-available/mokaair.conf (every EDIT marker).
  2. ln -s /etc/nginx/sites-available/mokaair.conf /etc/nginx/sites-enabled/   # if not linked
  3. nginx -t
  4. systemctl reload nginx
  5. Run the checks in ops/nginx/README.md -- especially the forged-address one, which is
     the only thing that proves per-source counting cannot be bypassed.
NEXT
