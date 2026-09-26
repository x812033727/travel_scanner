---
id: 2026-09-26-agy-account-json-lost-update
title: Antigravity account.json loses the plan when a status read races the quota probe
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-26T07:18:46Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/ai_accounts_agent/antigravity.py
  - apps/api/tests/test_ai_accounts_antigravity.py
---

# Antigravity account.json loses the plan when a status read races the quota probe

## Why

The required `api` check went red twice on pull requests that do not touch the AI accounts agent: #767 (skill descriptions only, 2026-09-25) and #790 (Claude usage probe logging, 2026-09-26). Both runs failed the same test:

```
FAILED tests/test_ai_accounts_antigravity.py::test_page_login_picks_google_takes_the_code_and_reads_the_quota
  - AssertionError: assert None == 'Ultra'   (test line 385)
```

A rerun passed both times, and main stayed green, so it looks like flakiness. It is a real lost update in the agent.

`AntigravityAccounts._remember` in `apps/api/ai_accounts_agent/antigravity.py` does an unlocked read-modify-write of the slot's `account.json`. It reads the file, merges the new values into that copy, and writes the whole copy back. Two threads call it for the same slot:

- The quota probe thread, in `refresh_usage`, calls `_remember(slot, email=email, plan=plan)` after it reads the TUI header. That happens before it types `/usage` and before `_record_usage` writes the windows.
- Every `status(slot)` call, from each `GET /v1/accounts` on the HTTP thread, calls `_remember(slot, email=email)` whenever the email in agy's logs differs from `account.json`.

The failing interleaving:

1. `status()` reads `account.json`, which has no plan yet.
2. The probe writes `{email, plan: "Ultra"}`.
3. `status()` writes back its stale copy plus the email.
4. `plan` is gone.
5. The probe then records the usage windows.

The test polls `GET /v1/accounts` in a tight loop until `usage` is set and then asserts the plan, so it reads exactly this state. On the host, the same race lets the admin AI settings page show an Antigravity account with usage but no plan until the next probe.

## Definition of done

- [ ] Concurrent `_remember` calls for the same slot never drop a key another call wrote. Every value written by either call survives both writes.
- [ ] A deterministic test reproduces the lost update on the current code and passes after the fix. It interleaves a `status()` write with a probe write, for example with a patched `_account` that pauses between the read and the write. It does not depend on timing luck.
- [ ] `test_page_login_picks_google_takes_the_code_and_reads_the_quota` no longer fails intermittently. It passes when the file is run in a loop.

## Steps

- [ ] Serialize the read-modify-write in `_remember`. The simplest fix is one `threading.Lock` per `AntigravityAccounts` instance, or per slot, held across `_account()` and `atomic_write_text`. The alternative is to stop `status()` from writing at all and let only the probe and the login remember the email.
- [ ] Check the Claude and Codex account stores for the same pattern: a read-modify-write of a shared JSON file from both the HTTP thread and a background thread. File a separate ticket for any you find instead of widening this one.
- [ ] Add the deterministic interleaving test described above.

## How to verify

```bash
cd apps/api
.venv/bin/python -m pytest tests/test_ai_accounts_antigravity.py -q
for i in $(seq 1 20); do .venv/bin/python -m pytest tests/test_ai_accounts_antigravity.py -q -k reads_the_quota || break; done
```

The file is POSIX-only (`posix_only`), so run it in CI or WSL, not on Windows.

## Notes

- CI evidence: #767 run 36171226813, api job 108190959590 (2026-09-25 18:28 UTC); #790 run 36225080052, api job 108357419279 (2026-09-26 07:15 UTC). Both passed on rerun.
- Found while watching CI for the merge-when-green subscription. The analysis reads `antigravity.py` on main at the time; line numbers will drift.
