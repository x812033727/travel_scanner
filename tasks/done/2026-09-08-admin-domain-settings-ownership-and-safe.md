---
id: 2026-09-08-admin-domain-settings-ownership-and-safe
title: Admin domain settings ownership and safe saves
status: done
priority: P1
area: api
owner: codex-admin-settings
claimed_at: 2026-09-08T10:04:05Z
created_at: 2026-09-08T10:03:38Z
completed_at: 2026-09-08T13:16:24Z
branch: codex/admin-domain-workspaces
depends_on: []
scope:
  - apps/web/components/header-session.tsx
  - apps/web/components/header-session-identity.test.tsx
  - apps/api/app/admin/service.py
  - apps/api/app/admin/schemas.py
  - apps/api/app/admin/router.py
  - apps/api/tests/test_admin_provider_settings.py
  - apps/api/tests/test_provider_settings_concurrency.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/web/lib/admin-settings-ownership.ts
  - apps/web/lib/admin-settings-ownership.test.ts
  - apps/web/lib/admin-settings-copy.ts
---

# Admin domain settings ownership and safe saves

## Why

A setting should have exactly one editable owner, and concurrent administrators or navigation must not silently lose drafts.

## Definition of done

- [x] Executable ownership registry routes domain fields and preserves all secrets/unknown fields in shared settings.
- [x] Dirty-only saves use compatible expected_updated_at with transaction/row locking and 409 conflicts.
- [x] Independent drafts survive tabs, Back/Forward and profile/currency updates.
- [x] Confirmed discard cannot be undone by a late usage response; session changes isolate secret drafts.
- [x] Full PR checks and authorized merge complete.

## Steps

- [x] Add ownership/status/deep links and individual provider saves.
- [x] Add first-row/existing-row PostgreSQL concurrency tests.
- [x] Introduce RAM-only HeaderSession identity, stable during profile updates and rotated at logout/new login.
- [x] Fix independent-review races and test them.

## How to verify

Run provider settings/concurrency pytest suites (RUN_INTEGRATION_TESTS=1 only on disposable PostgreSQL).
Run settings/ownership/header-session tests: focused set passed 81 cases.
Run whole-web TypeScript and ESLint.

## Notes

Provider secret drafts live only in a WeakMap keyed by active login identity; never localStorage/sessionStorage.
Omitting expected_updated_at is deliberately compatible with older clients. Provider snapshots keep masking and audit contracts.
