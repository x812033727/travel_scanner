---
id: 2026-09-09-admin-operations-center
title: Travel Scanner 後台營運中心升級
status: in-progress
priority: P1
area: api
owner: codex-root
claimed_at: 2026-09-09T02:26:21Z
created_at: 2026-09-09T02:25:54Z
completed_at:
branch: codex/admin-operations-center
depends_on: []
scope:
  - .env.example
  - README.md
  - docs/admin-operations-center.md
  - ops/deployer/README.md
  - apps/api
  - apps/web/app/[locale]/admin
  - apps/web/app/api/travel/[...path]
  - apps/web/components
  - apps/web/lib
  - apps/web/proxy.ts
  - apps/web/app/globals.css
---

# Travel Scanner 後台營運中心升級

## Why

The existing administration pages expose useful domain tools, but authorization is still a
single legacy flag, navigation and state feedback vary by page, member support lacks safe
lifecycle operations, and operators cannot inspect database health or request a verified backup.
The result is slow cross-page work and an unsafe gap between what the browser implies and what
the API authorizes.

## Definition of done

- [x] The API derives navigation and every management permission from effective capabilities.
- [x] Operators can filter and inspect users, then safely manage roles, suspension, sessions,
      verification, usage, and delayed erasure without bypassing owner/environment safeguards.
- [x] Database operators can inspect fixed PostgreSQL metrics and, only after all gates, request
      verified backups or controlled ANALYZE through the restricted host agent.
- [ ] Desktop and mobile administration flows are URL-restorable, accessible, localized, and
      covered by focused and full-stack checks.

## Steps

- [x] Add migration, capability roles, server bootstrap, audit query, and step-up session.
- [x] Extend the deployment agent with mutually exclusive verified backup and ANALYZE jobs.
- [x] Finish the unified shell, user drawer/actions, database center, and audit UI.
- [ ] Run backend, frontend, migration, browser, and CI validation; document rollout safeguards.

## How to verify

Run `uv run ruff check .`, `uv run mypy app`, and `uv run pytest` under `apps/api`; run
`npm run lint:web`, `npm run check:i18n`, `npm run typecheck:web`, `npm run test:web`,
`npm run build:web`, focused Playwright admin specs, Compose config, and the CI migration on a
fresh PostgreSQL service. In Chrome, walk the owner navigation and verify the database operator,
viewer, support, content, operations, and deployer boundaries at desktop and Pixel 7 widths.

## Notes

Work is isolated in `codex/admin-operations-center` from `98f8067b`. Docker is not installed on
the Windows host, so fresh PostgreSQL/Alembic and Compose build remain CI-enforced. Database and
deployment mutations intentionally have separate allowlists; a role capability alone is not an
execution grant.

The final concurrency hardening serializes database-operation terminal reconciliation and uses a
consistent `Job → User → AccountErasureRequest` lock order for erasure cancellation. The
PostgreSQL race regressions run in CI because the local Windows host has no PostgreSQL service.
