---
id: 2026-09-29-e2e-deploy-fixture-windows-mypy
title: Make the Unix-only e2e deploy-agent fixture type-check on Windows
status: done
priority: P3
area: api
owner: codex-windows-fixture
claimed_at: 2026-09-29T09:11:16Z
created_at: 2026-09-29T09:02:53Z
completed_at: 2026-09-29T09:18:17Z
branch: codex/admin-suspension-guards
depends_on: []
scope:
  - apps/api/tests/support/e2e_deploy_agent.py
  - apps/api/tests/test_e2e_deploy_agent_fixture.py
---

# Make the Unix-only e2e deploy-agent fixture type-check on Windows

## Why

Default Windows `mypy tests` fails at
`tests/support/e2e_deploy_agent.py:244`: `Name "socketserver.UnixStreamServer"
is not defined [name-defined]`. The e2e fixture deliberately uses a Unix socket
for Linux CI, but its unguarded server class is still type-checked on Windows.
This prevents a complete local type-check even when unrelated tests are sound.

## Definition of done

- [x] Default Windows `mypy tests` and Linux-targeted `mypy --platform linux tests`
      both pass without suppressing or excluding the entire fixture.
- [x] The existing fixture contract tests pass; Linux full-stack smoke still uses
      its original Unix socket protocol.
- [x] Unsupported platforms fail clearly before unlinking a socket path or binding
      a server; no TCP fallback or production deployment behavior is added.

## Steps

- [x] Check for active scope owners before modifying the fixture.
- [x] Add a platform guard that the type checker understands, preserving the
      existing Linux behavior, and cover unsupported-platform refusal.

## How to verify

From `apps/api`: `uv run mypy tests`, `uv run mypy --platform linux tests`,
`uv run pytest tests/test_e2e_deploy_agent_fixture.py -q` and scoped Ruff.
Use Linux CI full-stack smoke to verify the unchanged socket contract.

## Notes

Found while validating `2026-09-23-admin-owner-suspension-guards` on 2026-09-29.
Its full Windows mypy run reported this single error across 329 source files;
the modified security tests passed scoped mypy. The fixture is byte-identical
to main `ae5a04c7` and was last changed in PR #380. Other task notes mention
this problem, but no dedicated implementation task covered it. This is distinct
from the older Windows pytest collection failures in deployment-agent modules.

### Implementation and validation (2026-09-29)

- Rechecked both paths against main `09ce9586`, open PRs, remote branches and
  registered worktrees before claiming. No active overlapping implementation
  was found; the older site-experience task is open and unowned on current main.
- `main()` explicitly rejects Windows before environment validation, accessing
  the Unix server class, unlinking a socket or binding. The `else` branch keeps
  the original Linux server, permissions, HMAC handler and startup order. An
  early exception without the explicit `else` did not satisfy Windows mypy.
- Regression proof: the new Windows refusal test fails against the old helper
  (**1 failed / 2 passed**); after the guard, **3 passed / 0 skipped**. A sentinel
  file survives both Windows refusal and Linux's missing-fixture-flag refusal.
  Tests replace only the loaded module's `sys`, not global platform state.
- Complete default Windows `mypy tests` and Linux-targeted `mypy --platform linux
  tests` each pass **329 source files**, exit 0. Scoped Ruff check, format check
  and mypy also pass. Independent review found no actionable issue.
- A real local WSL/Python 3.14.4 run binds the unchanged Unix socket with mode
  `0660`: a correctly HMAC-signed `GET /v1/overview` returns 200 and the expected
  release/schema fields; an unsigned request returns 401. The server stays alive
  for both requests, then the dedicated process and temporary socket are cleaned
  up. This is a local fixture check, not full-stack or production acceptance.
- Included in draft PR #975, whose original validation exposed this issue.
  This closes the local implementation; fresh-head Linux CI full-stack smoke
  remains the integration gate and is not replaced by the platform unit tests.
