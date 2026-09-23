---
id: 2026-09-23-admin-owner-suspension-guards
title: Timed suspension and session revocation of owners skip step-up and environment guards
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-23T15:57:48Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/admin/user_router.py
  - apps/api/app/admin/users.py
  - apps/api/tests/test_admin_users.py
  - apps/api/tests/test_admin_users_integration.py
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

- [ ] A timed suspension of a user who holds `owner`, `deployer` or `database_operator`
      requires the same step-up as a permanent one (or a new `users.suspend_privileged`
      scope).
- [ ] `revoke_admin_user_sessions` and `unsuspend_admin_user` refuse environment-designated
      targets with `admin_environment_override`, and session revocation refuses the actor's
      own account.
- [ ] Existing support-role flows on ordinary members are unchanged.

## Steps

- [ ] `user_router.py`: load the target's roles before deciding whether to call
      `require_admin_step_up`; make the rule explicit in a helper next to the route.
- [ ] `users.py`: add the guards; reuse `_environment_designated`.
- [ ] Tests in `test_admin_users.py` (unit) and `test_admin_users_integration.py` (CI
      Postgres): support suspends an owner for 30 days without step-up and gets the step-up
      refusal; with step-up it succeeds; revoke on the env owner gets 409.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_admin_users.py -q && uv run ruff check . && uv run mypy app
```

## Notes

- Found in the 2026-09-23 security review (finding L1). Residual of R2-17 / API-10 from the
  earlier audits, not a regression: the step-up landed in September for roles, erasure and
  permanent suspension, and the timed path was left open on purpose for ordinary members.
