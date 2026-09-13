---
id: 2026-09-13-analytics-hash-key-separation
title: Analytics visitor hashing is keyed on APP_SECRET_KEY, so the signing key cannot be rotated alone
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-13T23:37:47Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/analytics/service.py
  - apps/api/app/config.py
  - apps/api/tests/test_analytics.py
---

# Analytics visitor hashing is keyed on APP_SECRET_KEY, so the signing key cannot be rotated alone

## Why

`app/analytics/service.py` derives both pseudonymous identifiers from the JWT signing key:

```python
session_hash = _digest(settings.app_secret_key, "analytics-session", str(payload.session_id))
visitor_hash = _digest(settings.app_secret_key, "analytics-day", f"{today}|{ip}|{ua}")
```

The privacy design is right — no raw IP is stored, the visitor hash rotates daily, DNT and
GPC are honoured. The problem is the key it borrows. `APP_SECRET_KEY` signs every access
token and every admin step-up token, so it is the one secret you most want to be able to
rotate on short notice: after a suspected leak, after an operator leaves, or just on a
schedule.

Rotating it today has a second, unrelated consequence: every `visitor_day_hash` and
`session_hash` computed after the rotation lands in a different keyspace from the rows
before it. Returning visitors read as new, sessions split across the boundary, and nothing
in the dashboard says that is what happened. The cost of an emergency rotation is therefore
partly paid in silently corrupted analytics, which is exactly the sort of coupling that
makes an operator hesitate at the moment they should not.

`docs/security-audit-2026-09.md` filed this as API-16 and recommendation #9.

## Definition of done

- [ ] `APP_SECRET_KEY` can be rotated without changing any analytics hash.
- [ ] Existing rows stay comparable to new ones, or the discontinuity is deliberate,
      one-off, and written down.
- [ ] Nothing else in the codebase uses `app_secret_key` for a purpose other than signing
      tokens.

## Steps

- [ ] Derive a dedicated key rather than adding another environment variable to set:
      HKDF from `SETTINGS_ENCRYPTION_KEY` with an `analytics` info string. `cryptography`
      is already a dependency. A separate `ANALYTICS_HASH_KEY` is also acceptable, but it
      is one more required production value and `validate_deployment_security` would have
      to enforce it.
- [ ] Replace both `app_secret_key` call sites in `analytics/service.py` (ingest at
      ~line 218, and the server-side path at ~line 379) with the derived key.
- [ ] Grep for other uses of `app_secret_key` and confirm each is token signing:
      `create_access_token`, `decode_access_token_claims`, `create_admin_step_up_token`,
      `require_admin_step_up`.
- [ ] Decide what happens to rows already hashed with the old key. The daily rotation means
      the visitor hash self-heals within a day; `session_hash` does not. Either accept one
      day of split sessions at deploy time, or keep reading with the old key for a
      transition window — and say which in the Notes.
- [ ] Document the rotation procedure in the runbook that covers `APP_SECRET_KEY`.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_analytics.py -q
```

Add a test that changes `app_secret_key` between two ingests and asserts the session and
visitor hashes are unchanged — that is the property this task exists to create, and it is
the one no current test covers.

## Notes

- Do not key it on `DATABASE_URL`, the site URL, or anything else that is not a secret.
  The whole point of a keyed hash here is that someone holding the analytics table cannot
  re-derive which IP produced which row.
- Filed by the 2026-09-13 security review (`docs/security-review-2026-09-13.md`).
