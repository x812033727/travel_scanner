# Mokaair deployment agent

The deployment button never mounts the Docker socket or a Git checkout into the API container.
This host-only agent owns those permissions and exposes four fixed operations through a Unix socket.

## Install

1. Create `/etc/travel-scanner/runtime.env` from the production application environment.
2. Run `sudo bash ops/deployer/install.sh` from a reviewed release.
3. Set a random 32+ character `DEPLOY_AGENT_HMAC_KEY` and a read-only GitHub Actions token in `/etc/travel-scanner/deployer.env`.
4. Put the same HMAC key, the socket path, `DEPLOYMENTS_ENABLED=true`, and `DEPLOY_ADMIN_EMAILS` in the application runtime environment.
5. Run `sudo systemctl enable --now travel-scanner-deployer` and inspect `systemctl status travel-scanner-deployer`.

Before enabling the Web button, run the same checks from the host account:

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

Before enabling the UI, keep `DEPLOYMENTS_ENABLED=false`, deploy this version manually, install the
agent, and verify the preflight endpoint. Backups are PostgreSQL custom-format dumps retained for the
latest seven deployments. Automatic rollback changes application images only; it never downgrades a
database migration or restores a dump.
