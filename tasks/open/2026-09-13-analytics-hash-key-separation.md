---
id: 2026-09-13-analytics-hash-key-separation
title: Analytics visitor hashing is keyed on APP_SECRET_KEY, so the signing key cannot be rotated alone
status: review
priority: P2
area: api
owner: claude-opus-5
claimed_at: 2026-09-14T00:41:24Z
created_at: 2026-09-13T23:37:47Z
completed_at:
branch: claude/security-check-o5zaj1
depends_on: []
scope:
  - apps/api/app/analytics/service.py
  - apps/api/app/config.py
  - apps/api/tests/test_analytics.py
  - docs/privacy-data-map.md
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

- [x] `APP_SECRET_KEY` can be rotated without changing any analytics hash.
- [x] Existing rows stay comparable to new ones — see "What happens to existing rows" below.
- [x] Nothing else in the codebase uses `app_secret_key` for a purpose other than signing
      tokens.

## Steps

- [x] Derived the key rather than adding another required production value:
      `Settings.analytics_hash_key` is one HMAC-SHA256 of `SETTINGS_ENCRYPTION_KEY` under the
      fixed label `mokaair:analytics-hash-key:v1`. No new environment variable, so nothing
      new can be left unset on a host.
- [x] Replaced both `app_secret_key` call sites in `analytics/service.py` — the ingest path
      and the server-side recording path.
- [x] Grepped every remaining use of `app_secret_key`: `create_access_token`,
      `decode_access_token_claims`, `create_admin_step_up_token`, `require_admin_step_up`,
      and `_fernet`'s non-production fallback. All token signing or encryption; none is an
      identity hash.
- [x] Decided what happens to rows already hashed with the old key — below.
- [x] Corrected `docs/privacy-data-map.md`, which documented the old key and named the
      coupling as a known side effect. A privacy document that describes the wrong key is
      worse than one that says nothing.

## Why one HMAC and not HKDF

HKDF has two steps and neither applies here. Extract condenses a non-uniform input; the
input is already a high-entropy random secret that production validation requires to be at
least 32 characters. Expand produces more than one hash length of output; the output is a
single 256-bit MAC key. What is left of HKDF in that case is exactly one HMAC with a
purpose label, which is what this does. Using `cryptography`'s HKDF would also have put that
import into `app/config.py`, which every process including the CLI and the workers loads.

The label is the part that matters: it pins the purpose, so the same secret used for
anything else cannot collide with this key, and `:v1` is where a deliberate re-key would
announce itself.

## What happens to existing rows

Both hashes change once, at deploy.

`visitor_day_hash` self-heals within a day — it already rotates on the Taipei date, so
rows before and after the deploy were never meant to be compared across that boundary.

`session_hash` does not: a session open across the deploy is counted as two. That is one
deploy's worth of split sessions, against a permanent property — and it is strictly better
than the alternative, which was to take the same hit on the day someone has to rotate the
signing key in a hurry. No transition window was built to read with the old key: it would
have meant keeping `app_secret_key` wired into analytics for the sake of one afternoon,
which is the coupling this task exists to remove.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_analytics.py -q
```

`test_rotating_the_signing_key_leaves_analytics_identities_intact` is the property this task
created, and no test covered it before: change `app_secret_key`, keep
`settings_encryption_key`, and both the derived key and the resulting digests are unchanged.

## Notes

- The key is not `SETTINGS_ENCRYPTION_KEY` either, only derived from it. Someone holding the
  analytics table and the derived key still cannot decrypt stored provider credentials or
  sign a token; `test_analytics_key_is_derived_rather_than_reused_and_moves_with_its_own_secret`
  pins that.
- `_digest` now takes the key instead of reading it. That is deliberate: a call site that
  reached for the wrong secret is exactly what went wrong here, and it would be invisible
  again if the lookup were hidden inside the function.
- Outside production `SETTINGS_ENCRYPTION_KEY` is optional and the signing key is the
  fallback. That is fine — development has one secret and no continuity to protect — and
  production forbids the case in `validate_deployment_security`.
- Filed by the 2026-09-13 security review (`docs/security-review-2026-09-13.md`).
