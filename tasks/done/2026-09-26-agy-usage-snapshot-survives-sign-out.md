---
id: 2026-09-26-agy-usage-snapshot-survives-sign-out
title: Antigravity usage snapshot is written back after a sign-out
status: done
priority: P3
area: api
owner: codex-agy-snapshot
claimed_at: 2026-09-29T11:52:40Z
created_at: 2026-09-26T15:24:16Z
completed_at: 2026-09-29T12:07:05Z
branch: codex/agy-usage-signout
depends_on: []
scope:
  - apps/api/ai_accounts_agent/antigravity.py
  - apps/api/tests/test_ai_accounts_antigravity.py
---

# Antigravity usage snapshot is written back after a sign-out

## Why

`AntigravityAccounts.logout()` in `apps/api/ai_accounts_agent/antigravity.py` unlinks the slot's usage snapshot (`SNAPSHOT_NAME`) outside any lock. Meanwhile the quota probe thread (`refresh_usage` → `_record_usage`) reads the previous snapshot and writes a new one. When a probe finishes after the sign-out, it writes the snapshot back with the old account's windows, and `slot_view` (`server.py`, the `usage` field) shows usage on a card that is signed out. A review of `2026-09-26-agy-account-json-lost-update` found this. That ticket fixed the same race for `account.json` and left the snapshot out of scope.

## Definition of done

- [x] A probe that finishes after `logout()` leaves no snapshot behind, and a signed-out slot reports no usage.
- [x] A deterministic test forces the interleaving: a paused `_record_usage` against `logout()`. It fails on the current code and passes after the fix.

## Steps

- [x] Take `AntigravityAccounts._account_lock` (added by the account.json fix) in `_record_usage` and around the snapshot unlink in `logout()`. Skip the write when `has_credentials(slot)` is false, the same way `_remember` does.
- [x] Add the test next to `test_a_status_read_does_not_write_the_account_back_after_a_sign_out`.

## How to verify

```bash
cd apps/api
.venv/Scripts/python.exe -m pytest tests/test_ai_accounts_antigravity.py -q
```

## Notes

- Low impact: it only shows stale numbers on a signed-out card, until the next sign-in overwrites them.
- 2026-09-29: Verified the original race with temporary dummy credential/snapshot files: logout removed the snapshot, then the paused probe recreated it; the signed-out slot still exposed usage. Checked active ancestor scopes, local branches/worktrees, remote heads and fully paginated PR files before claiming and again before preparing the PR; no competing change to the two scope files was found.
- `_record_usage` now holds the existing account lock while checking credentials and reading/updating/writing the snapshot. Logout removes both account metadata and the snapshot under that lock after deleting login files. The lock type and CLI probe lifecycle are unchanged.
- Four deterministic cases cover a late writer and an already-reading writer, each with fresh windows and with an error-only result that would restore previous windows. Events and a thin wrapper around the real lock control scheduling; worker failures are re-raised on the test thread, and cleanup releases and joins both workers. Assertions cover snapshot absence and the signed-out `slot_view` reporting no usage. A positive case confirms signed-in errors retain the last windows/time and later successful results replace them.
- RED on the original source: 4 failed, 15 passed, 6 POSIX skips, with all failures caused by the resurrected snapshot rather than timeouts. GREEN on Windows Python 3.13.15: 19 passed, 6 POSIX skips. Related account-agent, prompt-run, admin and subscription tests: 115 passed, 15 POSIX skips.
- Supplemental WSL Python 3.14.4 run: all 25 Antigravity tests passed with no skips, including six fake-CLI terminal cases. Source/test copy hashes matched the reviewed working tree; this supplements the matching Windows Python 3.13 run and does not replace Python 3.13 Linux CI.
- Independent in-memory mutation checks passed: removing the credential guard fails precisely the two late-writer cases; removing the record lock fails precisely the two in-flight cases. The signed-in positive case remains green, and repository source bytes were unchanged by mutation checks.
- Full API Ruff, `mypy app` (444 files), and scoped source/test mypy pass. Native Windows `mypy tests` reports the existing `tests/support/e2e_deploy_agent.py:244` UnixStreamServer platform error; PR #975 already carries its platform guard, so this ticket does not duplicate that change.
- Rebased onto main `9daa475f` before preparing the PR; neither the account-agent source/test inputs nor their dependencies changed. Final full API Ruff and `mypy tests --platform linux` pass (331 files). The Windows and WSL runs bind the unchanged final source/test hashes.
- All runs use local temporary fixtures and fake CLI programs; no real account login, production access or model call is part of this code fix.
