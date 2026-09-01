# Travel Scanner deployment agent

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

The token needs read-only access to repository Actions metadata. The repository, branch, workflow,
Compose project name, release paths, and health endpoints are compiled into the agent and cannot be
provided by a browser request. Agent upgrades remain a manual host administration action.

Before enabling the UI, keep `DEPLOYMENTS_ENABLED=false`, deploy this version manually, install the
agent, and verify the preflight endpoint. Backups are PostgreSQL custom-format dumps retained for the
latest seven deployments. Automatic rollback changes application images only; it never downgrades a
database migration or restores a dump.
