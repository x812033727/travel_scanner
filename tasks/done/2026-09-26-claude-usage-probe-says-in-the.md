---
id: 2026-09-26-claude-usage-probe-says-in-the
title: Claude usage probe says in the journal why it gave up
status: done
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-26T05:01:23Z
created_at: 2026-09-26T05:01:17Z
completed_at: 2026-09-26T05:19:25Z
branch: claude/ai-accounts-usage-probe-log
depends_on: []
scope:
  - apps/api/ai_accounts_agent/claude.py
  - apps/api/ai_accounts_agent/server.py
  - apps/api/ai_accounts_agent/security.py
  - apps/api/tests/test_ai_accounts_agent.py
  - ops/ai-accounts/README.md
---

# Claude usage probe says in the journal why it gave up

## Why

On 2026-09-26 slot `claude-b`'s usage snapshot stayed at 03:26:45Z. Two page-triggered
probes (about 04:36 and 04:52 UTC) got as far as the fallback message (history.jsonl held
"Reply with the single word: ok") but `ClaudeAccounts.refresh_usage` returned False, while
slots a and c refreshed at 04:52-04:53. `journalctl -u mokaair-ai-accounts` had nothing:
a False return leaves no trace, and `AgentApplication._refresh_usage` swallows every
exception with `contextlib.suppress(Exception)`. A manual run at 04:58 returned True (5h
0%, 7d 87%); its screen showed a weekly-limit notice and "auto mode unavailable for this
model" (the probe runs `--model haiku`), which may or may not explain the failures. Without
a log line the next failure cannot be diagnosed either.

## Definition of done

- [x] A probe that returns False writes one journal entry: slot, the reason (process
      exited with its code / timed out / login prompt / terminal closed), elapsed seconds,
      whether the fallback message was sent, and the last ~20 lines of the screen as drawn.
- [x] Nothing credential-like reaches the journal: lines pass `sanitize`, and anything that
      looks like an email address is replaced whole.
- [x] An exception in `_refresh_usage` is logged with its traceback instead of vanishing.

## Steps

- [x] `claude.py`: feed the probe's output into a `Screen` kept for the whole run, log on
      every False return.
- [x] `security.py`: `redact_emails`.
- [x] `server.py`: log exceptions in `_refresh_usage`.
- [x] Tests for the log line, the redaction and the exception path.
- [x] `ops/ai-accounts/README.md`: say what the journal shows.

## How to verify

`cd apps/api && uv run pytest tests/test_ai_accounts_agent.py` (the probe tests need a
POSIX terminal: run them in WSL or CI). On the host, after `ops/ai-accounts/install.sh`,
a failed probe shows up in `journalctl -u mokaair-ai-accounts`.

## Notes
- The probe now keeps a `Screen` (the same emulator the agy probe uses) for the whole
  run; the old flattened `output` buffer is cleared after each settled read and after
  the message, so it could not show the end of the run.
- When the CLI exits, reading the terminal usually fails (EIO) before `poll()` sees the
  exit; `_ended` waits up to a second for the exit code so the reason says
  `claude exited with code N` rather than `the terminal closed`. Output still in the
  terminal after an exit is drained into the screen first: the CLI's last words.
- The journal entry is one line (screen rows joined with ` | `, each cut to 200
  characters after `redact_emails`, then `sanitize`), so journald keeps it as one entry.
  `redact_emails` replaces the domain too, unlike antigravity's `mask_emails`.
- The exception log in `_refresh_usage` is `sanitize(redact_emails(traceback))` on one
  line, its last 4000 characters (the end names the exception).
- Verified: Windows `uv run pytest` on the four ai_accounts test files (POSIX ones skip),
  and in WSL with the dev-and-ci recipe, `tests/test_ai_accounts_agent*.py` and
  `test_ai_accounts_antigravity.py` 82 passed three runs in a row. Copy `ops/` into the
  WSL tree too, or the unit-file test fails on a missing path. One earlier WSL run failed
  `test_page_login_picks_google_takes_the_code_and_reads_the_quota` (plan None) and did
  not recur; it does not touch this change.
- Not done here: installing on the host (`ops/ai-accounts/install.sh`, owner approval).
  Once installed, the next failed probe of claude-b says why in
  `journalctl -u mokaair-ai-accounts`.
