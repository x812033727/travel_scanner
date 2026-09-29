---
id: 2026-09-29-e2e-deploy-fixture-windows-mypy
title: Make the Unix-only e2e deploy-agent fixture type-check on Windows
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-29T09:02:53Z
completed_at:
branch:
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

- [ ] Default Windows `mypy tests` and Linux-targeted `mypy --platform linux tests`
      both pass without suppressing or excluding the entire fixture.
- [ ] The existing fixture contract tests pass; Linux full-stack smoke still uses
      its original Unix socket protocol.
- [ ] Unsupported platforms fail clearly before unlinking a socket path or binding
      a server; no TCP fallback or production deployment behavior is added.

## Steps

- [ ] Check for active scope owners before modifying the fixture.
- [ ] Add a platform guard that the type checker understands, preserving the
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
