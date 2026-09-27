---
id: 2026-09-26-agy-account-json-lost-update
title: Antigravity account.json loses the plan when a status read races the quota probe
status: done
priority: P2
area: api
owner: claude-opus-agy-race
claimed_at: 2026-09-26T14:44:37Z
created_at: 2026-09-26T07:18:46Z
completed_at: 2026-09-26T15:24:33Z
branch: claude/agy-account-lost-update
depends_on: []
scope:
  - apps/api/ai_accounts_agent/antigravity.py
  - apps/api/tests/test_ai_accounts_antigravity.py
---

# Antigravity account.json loses the plan when a status read races the quota probe

## Why

The required `api` check went red three times on pull requests that do not touch the AI accounts agent: #767 (2026-09-25), #790 and #808 (2026-09-26). Each time the failing test was `test_page_login_picks_google_takes_the_code_and_reads_the_quota`, with `assert None == 'Ultra'`. When this ticket was filed, the cause was taken to be a lost update in `AntigravityAccounts._remember`. **That was wrong for the CI failures.** An independent review traced them to a different cause:

- **What `status()` actually did.** In that test `status()` never calls `_remember` during the probe. `finalize` already saved the email and cached the status for `agy_cache_seconds` (30 s), and every overview during the probe reads that cache.
- **The real cause: a stale-cache window.** `_record_usage` writes the snapshot, then `_stop_session` kills the TUI and waits up to 3 s, and only after that is the status cache invalidated. The old test waited only for `usage`, so it read the cached status from before the probe, where `plan` was still `None`.
- **Already fixed.** #810 (`06f0cd50`, merged 2026-09-26 14:40 UTC) changed the test to wait for `not usage_refreshing` as well. All three failing runs used the pre-#810 test line.

The lost update this ticket describes is real, though it is narrow. `_remember` read `account.json`, changed it, and wrote the whole file back with no lock. Two threads call it for the same slot:

- the quota probe thread, with the plan;
- a `status()` on a request thread, whenever the email in agy's logs differs from the file.

A `status()` that read the file before the probe saved the plan wrote its stale copy back over the plan. A `status()` that read the file before `logout()` wrote the account back after the sign-out.

## Definition of done

- [x] Concurrent `_remember` calls for the same slot never drop a key another call wrote, and a sign-out is never undone by a write that started before it.
- [x] Deterministic tests force both interleavings with events and a patched `_account`. They fail 5/5 on the old code and pass 10/10 on the new code. An exception inside the paused thread now fails the test instead of being swallowed as a warning.
- [x] ~~`test_page_login_picks_google_takes_the_code_and_reads_the_quota` no longer fails intermittently~~. This was never this bug; #810 fixed it (see Why).

## Steps

- [x] Take one `threading.Lock` per `AntigravityAccounts` (one instance per agent process, `server.py:143`) across `has_credentials` + `_account` + write in `_remember`. Take it in `logout()` around the unlink of `account.json`, after the token files are gone. `_remember` stops when the slot has no credentials.
- [x] Check the Claude and Codex account stores for the same pattern. Their `status()` runs the CLI (`claude auth status`) or reads without writing, so neither has it.
- [x] Add the two interleaving tests.

## How to verify

```bash
cd apps/api
.venv/Scripts/python.exe -m pytest tests/test_ai_accounts_antigravity.py -q -k "never_writes_back or after_a_sign_out"
.venv/Scripts/python.exe -m pytest tests/test_ai_accounts_agent.py tests/test_ai_accounts_agent_runs.py tests/test_ai_accounts_antigravity.py tests/test_ai_accounts_admin.py -q
```

The two new tests need no terminal and also run on Windows.

## Notes

- Review (2026-09-26) checked for deadlocks and found none. `_account_lock` is a leaf lock: while it is held, only `Path.exists`, `read_json`, `atomic_write_text` and `unlink` run. Every caller of `status()`, `_remember`, `logout` and `refresh_usage` was traced, and no thread holding the lock waits on another one. `mokaair-account.json` has no other writers anywhere in the repository.
- The usage snapshot has the same shape of race. `logout()` unlinks `SNAPSHOT_NAME` outside any lock, while a probe that finishes after the sign-out rewrites it with the old account's windows. It is filed separately as `2026-09-26-agy-usage-snapshot-survives-sign-out` rather than widening this change.
