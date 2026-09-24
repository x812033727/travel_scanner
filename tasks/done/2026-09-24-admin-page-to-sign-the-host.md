---
id: 2026-09-24-admin-page-to-sign-the-host
title: Admin page to sign the host's Claude and Codex CLIs in and show each account's quota
status: done
priority: P2
area: web
owner: claude-opus-5-5
claimed_at: 2026-09-24T08:38:20Z
created_at: 2026-09-24T08:37:58Z
completed_at: 2026-09-24T09:00:29Z
branch: claude/ai-accounts-admin
depends_on: []
scope:
  - apps/api/app/ai_accounts
  - apps/api/app/config.py
  - apps/api/app/main.py
  - apps/api/app/admin/operations_service.py
  - apps/api/tests/test_ai_accounts_admin.py
  - apps/api/tests/test_admin_operations.py
  - apps/api/tests/test_admin_rbac.py
  - apps/api/tests/test_security_config.py
  - .env.example
  - docker-compose.prod.yml
  - apps/web/app/[locale]/admin/ai-accounts
  - apps/web/components/admin-ai-accounts-panel.tsx
  - apps/web/components/admin-ai-accounts-panel.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/lib/admin-operations.ts
  - apps/web/components/admin-nav.tsx
  - apps/web/app/api/travel/[...path]/route.ts
  - tools/e2e-runtime-api.mjs
  - apps/web/e2e/admin-operations.spec.ts
  - apps/web/e2e/admin-operations-full-stack.spec.ts
---

# Admin page to sign the host's Claude and Codex CLIs in and show each account's quota

## Why

The owner runs Claude Code and Codex as root over SSH on the production host on their
subscriptions, and asked to do the sign-in from the website, to keep several accounts per
tool (two, then "even three") with a default, and to see each account's name and remaining
quota. The host half, an agent that owns the CLIs and answers signed requests on a Unix
socket, is `2026-09-24-host-agent-that-logs-the-root` (PR #728). This ticket is the site half:
the API routes that relay to that socket, the Compose mount, and `/admin/ai-accounts`.

## Definition of done

- [x] `/admin/ai-accounts` lists, per tool, every signed-in account, the default and any open
      login, with email, plan and the remaining share of each quota window, plus the reset
      time; Claude's snapshot shows when it was taken and "reset" once its window has passed.
- [x] From the page the owner can add an account in the next free slot (up to five per
      tool), finish a Codex device-code login or a Claude paste-the-code login, cancel it,
      sign an account out after a confirmation, and make an account the default.
- [x] Only the owner reaches the routes (`roles.manage`, required by the router itself and
      locked by the RBAC table test); other admins get 403 and the agent is never called.
- [x] The page states it plainly when the feature is off, the agent is unreachable, or the
      host has no account allowlist; the pasted code is never logged or audited, and no
      field the API does not know is passed from the agent to the browser.

## Steps

- [x] API: settings with production validation, signed client over the socket, owner-only
      router, audit rows for login start and end (once per login), logout and default.
- [x] `docker-compose.prod.yml`: mount `/run/mokaair-ai-accounts` read-only into `api`.
- [x] Web: page, panel, five-language messages, navigation registration in all five places,
      a 30 s proxy timeout for these routes.
- [x] Tests: API routes with a signature-checking fake agent, config validation, RBAC,
      registry; the panel's display, both login flows, sign-out and default.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests   && uv run pytest tests/test_ai_accounts_admin.py tests/test_security_config.py      tests/test_admin_rbac.py tests/test_admin_operations.py
npm run lint:web && npm run check:i18n && npm run typecheck:web
cd apps/web && npx vitest run components/admin-ai-accounts-panel.test.tsx
```

The page was also driven in the in-app browser against a mock of the agent (desktop and
390 px, no horizontal overflow): Codex device code to success, Claude code to success.

## Notes

- The feature ships off (`AI_ACCOUNTS_ENABLED=false`); with it off the page only says how to
  turn it on. The rollout on the host is `2026-09-24-roll-out-the-ai-accounts-agent`.
- The proxy's 30 s budget covers the API's 25 s agent timeout, which covers the agent's
  worst case for starting a login (a Claude CLI start, or a Codex app-server handshake plus
  `account/login/start`).
- An audit row for a finished login is written by the first poll that sees it end; a second
  concurrent poll could in principle write a duplicate row. There is no unique index for it
  because that would need a migration for a cosmetic case.
