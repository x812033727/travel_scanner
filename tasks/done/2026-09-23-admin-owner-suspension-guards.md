---
id: 2026-09-23-admin-owner-suspension-guards
title: Timed suspension and session revocation of owners skip step-up and environment guards
status: done
priority: P2
area: api
owner: codex-admin-guards
claimed_at: 2026-09-29T08:51:22Z
created_at: 2026-09-23T15:57:48Z
completed_at: 2026-09-29T09:06:11Z
branch: codex/admin-suspension-guards
depends_on: []
scope:
  - apps/api/app/admin/user_router.py
  - apps/api/app/admin/users.py
  - apps/api/tests/test_admin_users.py
  - apps/api/tests/test_admin_users_integration.py
  - apps/web/components/admin-users-panel.tsx
  - apps/web/components/admin-users-panel.test.tsx
---

# Timed suspension and session revocation of owners skip step-up and environment guards

## Why

`POST /admin/users/{id}/suspension` requires the `users.suspend_permanent` step-up only when
`suspended_until` is `None` (`user_router.py`). A timed suspension of up to
`MAX_TIMED_SUSPENSION` (90 days) needs only the `users.manage` capability, which the `support`
role holds. `_suspend_admin_user_serialized` refuses self, environment-designated accounts and
the last owner, so a support admin cannot lock out the last owner, but can lock out any other
database-assigned `owner`, `deployer` or `database_operator` for 89 days (the `auth_version`
bump ends their sessions at once), and only another owner can undo it.

`POST /{id}/sessions/revoke` and `DELETE /{id}/suspension` have no self or
environment-designated guard at all, so the same role can force-log-out the environment owner
in a loop, or lift a suspension an owner imposed. Every action is audit-logged, which is why
this is Low rather than Medium, but a hijacked support session should not be able to remove
the people who would investigate it.

## Definition of done

- [x] A timed suspension of a user who holds `owner`, `deployer` or `database_operator`
      requires the same step-up as a permanent one (or a new `users.suspend_privileged`
      scope).
- [x] `revoke_admin_user_sessions` and `unsuspend_admin_user` refuse environment-designated
      targets with `admin_environment_override`, and session revocation refuses the actor's
      own account.
- [x] Existing support-role flows on ordinary members are unchanged.

## Steps

- [x] Evaluate fresh target roles under the existing owner mutation guard and row
      locks, then call the route-provided step-up verifier before mutation.
      Checking roles before taking the guard would race with a role grant.
- [x] `users.py`: add the guards; reuse `_environment_designated`.
- [x] Tests in `test_admin_users.py` (unit) and `test_admin_users_integration.py` (CI
      Postgres): support suspends an owner for 30 days without step-up and gets the step-up
      refusal; with step-up it succeeds; revoke on the env owner gets 409.
- [x] Connect timed suspension to the existing password-confirmation dialog when
      verification is required, preserving the requested deadline and target.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_admin_users.py -q && uv run ruff check . && uv run mypy app
```

## Notes

- Found in the 2026-09-23 security review (finding L1). Residual of R2-17 / API-10 from the
  earlier audits, not a regression: the step-up landed in September for roles, erasure and
  permanent suspension, and the timed path was left open on purpose for ordinary members.
- 2026-09-29: fresh main `ae5a04c7` still has the issue. No active overlapping
  claim, open PR or new worktree change was found. Old OneDrive changes are
  already-merged August usage-management work and remain untouched.
- Scope includes the existing user panel and its tests so a timed operation can
  finish the required password verification. Use a snapshot of the target,
  deadline, reason and idempotency key; it must never become a permanent suspension.
- Keep the existing permanent-suspension route check. The added verifier is
  mandatory for a privileged timed suspension, even for a direct service call;
  no verifier means `admin_step_up_required`. Both target and role rows must be
  refreshed under the shared owner mutation guard before deciding.

### Implementation and validation

- The route supplies the existing `users.suspend_permanent` verifier. Privileged
  timed suspension checks it inside the shared mutation guard, after target and
  role rows are locked and refreshed. Missing callbacks fail closed. Permanent
  suspension retains its original route-level step-up check.
- Environment-designated accounts are rejected before unsuspension or session
  revocation writes; self revocation returns the existing `admin_self_action`.
- The UI handles required, invalid and wrong-scope challenges. Its read-only
  pending snapshot preserves id, email, reason, deadline and idempotency key;
  verification never converts a timed suspension to permanent. The dialog shows
  the original deadline/reason, and cancellation or changing users invalidates it.
- Real SQLite regression tests: original code **20 failed / 20 passed**;
  fixed user tests **40 passed**. Including existing RBAC and integration collection,
  the focused run is **94 passed / 5 skipped**. Rejecting an operation leaves
  persisted suspension fields, auth version and audit records unchanged.
- Two new PostgreSQL cases use `pg_blocking_pids` to prove suspension waits for
  a real role-grant transaction. They cover a new assignment and renewal of a
  preloaded expired assignment. The local skips include these two plus three
  pre-existing integration cases; actual PG execution remains a CI requirement.
- UI regression tests: original code **6 failed / 17 passed**; fixed code
  **23 passed**, using bundled Node 24.21.0 and Vitest 5.0.2. Scoped ESLint,
  full web TypeScript, full API Ruff and `mypy app` (443 files) passed.
- Scoped mypy for both modified API test files passed. The initial default
  Windows run exposed an existing Unix socket fixture typing error. Follow-up
  `2026-09-29-e2e-deploy-fixture-windows-mypy`, included in the same PR, fixes
  that error with an explicit platform branch and three passing contract tests.
  Complete Windows and Linux-targeted `mypy tests` now each pass all 329 files.
- Independent API, UI and regression review found no blocking issue. These are
  local tests and review results; production access and browser acceptance are
  outside this change.
