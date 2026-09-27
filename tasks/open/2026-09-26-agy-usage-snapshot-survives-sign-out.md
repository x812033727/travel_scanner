---
id: 2026-09-26-agy-usage-snapshot-survives-sign-out
title: Antigravity usage snapshot is written back after a sign-out
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-26T15:24:16Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/ai_accounts_agent/antigravity.py
  - apps/api/tests/test_ai_accounts_antigravity.py
---

# Antigravity usage snapshot is written back after a sign-out

## Why

`AntigravityAccounts.logout()` in `apps/api/ai_accounts_agent/antigravity.py` unlinks the slot's usage snapshot (`SNAPSHOT_NAME`) outside any lock. Meanwhile the quota probe thread (`refresh_usage` → `_record_usage`) reads the previous snapshot and writes a new one. When a probe finishes after the sign-out, it writes the snapshot back with the old account's windows, and `slot_view` (`server.py`, the `usage` field) shows usage on a card that is signed out. A review of `2026-09-26-agy-account-json-lost-update` found this. That ticket fixed the same race for `account.json` and left the snapshot out of scope.

## Definition of done

- [ ] A probe that finishes after `logout()` leaves no snapshot behind, and a signed-out slot reports no usage.
- [ ] A deterministic test forces the interleaving: a paused `_record_usage` against `logout()`. It fails on the current code and passes after the fix.

## Steps

- [ ] Take `AntigravityAccounts._account_lock` (added by the account.json fix) in `_record_usage` and around the snapshot unlink in `logout()`. Skip the write when `has_credentials(slot)` is false, the same way `_remember` does.
- [ ] Add the test next to `test_a_status_read_does_not_write_the_account_back_after_a_sign_out`.

## How to verify

```bash
cd apps/api
.venv/Scripts/python.exe -m pytest tests/test_ai_accounts_antigravity.py -q
```

## Notes

- Low impact: it only shows stale numbers on a signed-out card, until the next sign-in overwrites them.
