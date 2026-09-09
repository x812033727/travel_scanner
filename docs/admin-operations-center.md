# Administration operations center

The administration area is a capability-gated operations console. Navigation is returned by
`GET /api/v1/admin/bootstrap`; the web application never infers access from a role name. Every
administration endpoint repeats the authorization check on the API.

## Roles and compatibility

Non-owner roles are additive and may expire. The `owner` role is deliberately permanent so an
expired recovery assignment can never strand the console without a durable owner. `ADMIN_EMAILS`
remains the recovery mechanism and grants an effective, immutable `owner` role while the address
is present in the environment. Legacy
`users.is_admin=true` accounts are migrated to `support`, `content`, and `operations`; they do not
silently receive database or deployment access. The legacy `set-admin --revoke` command removes
only those three `legacy_backfill` assignments and preserves roles granted explicitly in the UI.

The API expands effective roles into the exact capability sets below. This block is intentionally
machine-checked against `ADMIN_ROLE_CAPABILITIES`, so documentation and endpoint authorization
cannot drift unnoticed.

<!-- admin-role-capabilities:start -->
| Role | Effective capabilities |
| --- | --- |
| `viewer` | `admin.access`, `analytics.read`, `audit.read`, `community.read`, `content.read`, `dashboard.read`, `settings.read`, `users.read` |
| `support` | `admin.access`, `audit.read`, `community.manage`, `community.read`, `dashboard.read`, `usage.manage`, `users.manage`, `users.read` |
| `content` | `admin.access`, `audit.read`, `community.read`, `content.manage`, `content.read`, `dashboard.read` |
| `operations` | `admin.access`, `analytics.read`, `audit.read`, `dashboard.read`, `settings.manage`, `settings.read` |
| `database_operator` | `admin.access`, `audit.read`, `dashboard.read`, `database.maintain`, `database.read` |
| `deployer` | `admin.access`, `audit.read`, `dashboard.read`, `deploy.execute`, `deploy.read` |
| `owner` | `admin.access`, `analytics.read`, `audit.read`, `community.manage`, `community.read`, `content.manage`, `content.read`, `dashboard.read`, `database.maintain`, `database.read`, `deploy.execute`, `deploy.read`, `roles.manage`, `settings.manage`, `settings.read`, `usage.manage`, `users.manage`, `users.read` |
<!-- admin-role-capabilities:end -->

All roles except `owner` may have an expiry. Database maintenance and deployment execution also
require their separate environment allowlist, feature flag, healthy agent, and
operation-specific authentication described below.

Database maintenance requires all of the following:

1. the `database.maintain` capability, granted by `database_operator` or `owner`;
2. membership in `DATABASE_ADMIN_EMAILS`;
3. `ADMIN_DATABASE_MAINTENANCE_ENABLED=true`;
4. a healthy, authenticated deployment agent; and
5. a five-minute, operation-scoped password step-up.

Deployment keeps its independent `DEPLOY_ADMIN_EMAILS` gate. Environment allowlists cannot be
changed from the web interface.

## Step-up and destructive account actions

`POST /api/v1/admin/step-up` verifies the administrator's current password and issues a five-minute
HttpOnly cookie scoped to the requested operation. The token is bound to the administrator and the
current `auth_version`; changing the password or forcing a logout invalidates it. SSO-only
administrators must establish a local password first. Use the ordinary forgot-password and
reset-password flow to create it; do not share a temporary password. Before assigning an
operational role, production must have `COMMUNITY_SMTP_HOST` and a non-empty
`COMMUNITY_MAIL_FROM`, verified outbound delivery to every intended operator, and the operator's
account response must list `password` in `auth_methods`. Otherwise deployment and database
step-up cannot succeed.

Role changes, permanent suspension, and scheduled account erasure require an idempotency key,
reason, typed confirmation, and the matching step-up scope. An account erasure has a 24-hour grace
period and reuses the durable erasure worker. The system rejects self-erasure, environment owners,
and any operation that would remove the last owner. A timed suspension may be at most 90 days;
longer restrictions use the password-confirmed permanent-suspension flow.

## Database center safety boundary

`/admin/database` exposes health, Alembic revision, storage and connection metrics, public-schema
table statistics, verified backup metadata, and the controlled `ANALYZE` operation. It deliberately
does not expose:

- arbitrary SQL or identifiers supplied by a browser;
- table rows;
- backup download, deletion, or online restore;
- `VACUUM FULL`, `REINDEX`, or arbitrary migration versions.

Manual backups and `ANALYZE` run in the host deployment agent. The agent serializes them with
deployments using the same host lock. Backups use PostgreSQL custom format, are checked with
`pg_restore --list`, receive a SHA-256 checksum, and retain the newest seven files. A missing agent,
`pg_dump`, `pg_restore`, allowlist, or feature flag is reported as unavailable; the API never returns
a fabricated success.

## Initial rollout

1. Deploy the schema and UI with both `DEPLOYMENTS_ENABLED=false` and
   `ADMIN_DATABASE_MAINTENANCE_ENABLED=false`.
2. Confirm the legacy role backfill and `/admin/audit` records on the production database.
3. Configure and test SMTP, then use the password-recovery flow for every SSO-only operator and
   verify that `auth_methods` includes `password`.
4. Assign the least-privilege role and matching allowlist: `deployer` plus
   `DEPLOY_ADMIN_EMAILS`, `database_operator` plus `DATABASE_ADMIN_EMAILS`, or both only when the
   same person genuinely needs both surfaces.
5. Upgrade and preflight the host agent from a reviewed release while both feature flags remain
   disabled.
6. Select the deployment-only, database-only, or combined profile in
   `ops/deployer/README.md`, restart the API, and confirm the unrelated surface remains disabled.
7. For database maintenance, run a manual backup during a maintenance window and independently
   verify its full checksum and `pg_restore --list` result with the host commands in that runbook.
8. Permit `ANALYZE` only after the verified backup and audit record have been reviewed.

Keep database migrations backward compatible: application rollback never downgrades the database.
