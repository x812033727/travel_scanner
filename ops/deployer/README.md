# Mokaair deployment agent

The deployment button never mounts the Docker socket or a Git checkout into the API container.
This host-only agent owns those permissions and exposes only fixed deployment, verified-backup,
and `ANALYZE` operations through a Unix socket. It does not accept SQL, repository locations,
backup paths, restore requests, or shell commands from the API or browser.

## Install

1. Create `/etc/travel-scanner/runtime.env` from the production application environment.
2. Run `sudo bash ops/deployer/install.sh` from a reviewed release.
3. Set a random 32+ character `DEPLOY_AGENT_HMAC_KEY` and a read-only GitHub Actions token in `/etc/travel-scanner/deployer.env`.
4. Put the same HMAC key and the fixed
   `DEPLOY_AGENT_SOCKET=/run/travel-scanner-deployer/deployer.sock` in the application runtime
   environment. Keep both `DEPLOYMENTS_ENABLED=false` and
   `ADMIN_DATABASE_MAINTENANCE_ENABLED=false` during installation and preflight.
5. Run `sudo systemctl enable --now travel-scanner-deployer` and inspect `systemctl status travel-scanner-deployer`.

Before enabling either operation surface, run the same checks from the host account:

```bash
sudo -u travel-deployer bash -lc \
  'cd /opt/travel-scanner-deployer && set -a && source /etc/travel-scanner/deployer.env && set +a && python3 -m deployment_agent preflight'
```

After manually deploying this same latest-green `main`, initialize the agent's
`current` pointer once. This command accepts no repository, branch, or SHA; it
resolves the pinned latest-green main itself and refuses to overwrite an existing
pointer:

```bash
sudo -u travel-deployer bash -lc \
  'cd /opt/travel-scanner-deployer && set -a && source /etc/travel-scanner/deployer.env && set +a && python3 -m deployment_agent bootstrap-current'
```

The token needs read-only access to repository Actions metadata: use a fine-grained personal access
token scoped to this repository with only `Actions: Read`. The repository, branch, workflow,
Compose project name, release paths, and health endpoints are compiled into the agent and cannot be
provided by a browser request. Agent upgrades remain a manual host administration action.

The socket and SQLite state paths are intentionally fixed by the reviewed systemd unit. Do not
add `DEPLOY_AGENT_SOCKET` or `DEPLOY_AGENT_STATE` to `deployer.env`; the agent refuses overrides
that would disagree with `ReadWritePaths` or the Compose mount. The application-side
`DEPLOY_AGENT_SOCKET` must use the fixed path above.

## Enablement profiles

The two feature flags and allowlists are independent. An allowlist entry is not a role assignment:
deployment also requires the effective `deployer` or `owner` role, while database maintenance
requires `database_operator` or `owner`. Start with the narrowest profile, restart the API after
changing its runtime environment, and check the bootstrap response before asking an operator to
use the UI.

Deployment only:

```dotenv
DEPLOYMENTS_ENABLED=true
DEPLOY_ADMIN_EMAILS=deploy@example.com
ADMIN_DATABASE_MAINTENANCE_ENABLED=false
DATABASE_ADMIN_EMAILS=
```

Database only:

```dotenv
DEPLOYMENTS_ENABLED=false
DEPLOY_ADMIN_EMAILS=
ADMIN_DATABASE_MAINTENANCE_ENABLED=true
DATABASE_ADMIN_EMAILS=database@example.com
```

Combined, only for an operator who needs both responsibilities:

```dotenv
DEPLOYMENTS_ENABLED=true
DEPLOY_ADMIN_EMAILS=deploy-and-database@example.com
ADMIN_DATABASE_MAINTENANCE_ENABLED=true
DATABASE_ADMIN_EMAILS=deploy-and-database@example.com
```

All three profiles also require the shared 32+ character `DEPLOY_AGENT_HMAC_KEY` and fixed
`DEPLOY_AGENT_SOCKET` in the application runtime environment. The agent environment requires the
same HMAC key and its read-only GitHub token; it must not contain socket or state overrides.

Deployment requests and database mutations require a local-password check. For an SSO-only
operator, use the ordinary forgot-password and reset-password flow before enablement. That flow
requires a working `COMMUNITY_SMTP_HOST`, a non-empty `COMMUNITY_MAIL_FROM`, and verified mail
delivery. Confirm the operator's account response includes `password` in `auth_methods` before
enabling either feature; an SSO session by itself cannot satisfy the check.

## Verify a manual backup on the host

The UI reports the filename and full SHA-256 from the agent's verified catalog. An operator can
independently verify the newest retained dump without exposing it through the browser:

```bash
backup_file="$(
  sudo -u travel-deployer find /var/backups/travel-scanner -maxdepth 1 -type f \
    -name 'travel-scanner-*.dump' -printf '%T@ %p\n' \
    | sort -nr | head -n 1 | cut -d' ' -f2-
)"
test -n "${backup_file}" && test -f "${backup_file}"
sudo -u travel-deployer sha256sum -- "${backup_file}"
sudo -u travel-deployer bash -c '
  set -euo pipefail
  backup_file="$1"
  cd /srv/travel-scanner/current
  set -a
  source /etc/travel-scanner/runtime.env
  set +a
  RUNTIME_ENV_FILE=/etc/travel-scanner/runtime.env \
    docker compose -p travel-scanner -f docker-compose.prod.yml \
      exec -T postgres pg_restore --list < "${backup_file}" >/dev/null
' bash "${backup_file}"
```

A zero exit status confirms that the retained file is readable as a PostgreSQL custom-format
archive. Compare the complete `sha256sum` output, filename, schema revision, and release SHA with
the authenticated `GET /api/v1/admin/database/backups` record; do not compare against a truncated
table cell. Periodically perform a restore drill into a disposable, access-restricted PostgreSQL
instance during a maintenance window. Never restore over production, and never treat
`pg_restore --list` alone as proof that a restore drill succeeded.

## Trust boundary

- `travel-deployer` belongs to the `docker` group, and access to the Docker socket is
  root-equivalent on the host. The systemd hardening in the unit file restricts the agent process
  itself, not the containers it is allowed to start, so treat `DEPLOY_AGENT_HMAC_KEY` and
  membership in the `travel-api` group as host root credentials. If that is not acceptable, run a
  rootless Docker daemon or a socket proxy that exposes only the Compose endpoints the agent uses.
- `/etc/travel-scanner` is `root:travel-deployer` with mode `0750`; `deployer.env` and
  `runtime.env` are `0640`. The installer re-applies these permissions on every run, so re-run it
  after editing the files by hand, and never widen the directory to world-readable.
- `/run/travel-scanner-deployer` is recreated by `ExecStartPre` on every start with the
  `travel-api` group so that the API container keeps socket access after a reboot.
- After changing the unit file, the installer, or the agent code, re-run the `preflight` command
  shown above before enabling the web button again.

Before enabling the UI, keep `DEPLOYMENTS_ENABLED=false` and
`ADMIN_DATABASE_MAINTENANCE_ENABLED=false`, deploy this version manually, install the agent, and
verify the preflight endpoint. Deployment and manual database work share one non-blocking host file
lock, so neither can overlap the other. Backups are PostgreSQL custom-format dumps, validated with
`pg_restore --list`, hashed with SHA-256, and retained to the newest seven files. Automatic rollback
changes application images only; it never downgrades a database migration or restores a dump. The
administration UI intentionally provides no backup download, deletion, or restore endpoint.
