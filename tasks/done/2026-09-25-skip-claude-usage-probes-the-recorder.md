---
id: 2026-09-25-skip-claude-usage-probes-the-recorder
title: Skip Claude usage probes the recorder would not write, and log probe failures
status: done
priority: P3
area: ops
owner: claude-opus-5-5
claimed_at: 2026-09-26T14:49:55Z
created_at: 2026-09-25T01:33:21Z
completed_at: 2026-09-26T15:07:48Z
branch: claude/ai-accounts-probe-throttle
depends_on: []
scope:
  - apps/api/ai_accounts_agent/server.py
  - apps/api/ai_accounts_agent/claude.py
  - apps/api/tests/test_ai_accounts_agent.py
  - apps/api/tests/test_ai_accounts_agent_runs.py
  - ops/ai-accounts/README.md
---

# Skip Claude usage probes the recorder would not write, and log probe failures

## Why

Found on 2026-09-25 while checking the automatic Claude usage probes (#737) on the host.

- **The recorder throttles itself.** `statusline.record_snapshot` skips rewriting a snapshot
  whose numbers are unchanged within `UNCHANGED_REWRITE_SECONDS` (60 s). The status line
  redraws every few seconds, and the throttle keeps it from writing each time.
- **The probe misreads that as a failure.** `ClaudeAccounts.refresh_usage` only counts success
  when the snapshot file changes. A probe that starts less than 60 s after the last snapshot
  therefore never sees a change. It waits 15 s, sends its one fallback message (a small
  quota cost), waits 40 s more and returns False. The numbers on the page were current all
  along.
- **When it happens.** Page views cannot trigger it: they need the snapshot to be 30 minutes
  old. The refresh button can, if it is pressed within a minute of a Claude session over SSH
  updating the snapshot, because the button's minimum interval only counts the agent's own
  attempts.
- **Failures leave no trace.** `AgentApplication._refresh_usage` suppresses every exception
  and nothing is logged. When a probe fails for a real reason (the TUI changed, a token
  refresh error), the journal says nothing and the page just keeps its old numbers.
  Reproducing a probe by hand (`scratchpad` script driving `refresh_usage` with a logged
  `os.read`) was the only way to see what happened.

## Definition of done

- [x] `maybe_refresh_usage` does not start a probe, forced or not, while the snapshot is
      younger than the recorder's rewrite interval.
- [x] A probe that returns False or raises writes one line to stderr (the journal):
      slot, reason and duration, with no screen text (it can echo codes or emails).
- [x] Tests cover both.

## Steps

- [x] Share the interval: import `UNCHANGED_REWRITE_SECONDS` from `statusline` in `server.py`.
- [x] Have `refresh_usage` return a reason (`no_change`, `login_picker`, `exited`,
      `timeout`) instead of a bare bool, and log it.
- [x] Tests with the fake interactive CLI and the `RecordingAccounts` stand-in.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_ai_accounts_agent.py
```

On the host, `journalctl -u mokaair-ai-accounts` shows a line for any failed probe.

## Notes

- Everything else checked out on the host. Background probes updated all three Claude snapshots
  within the systemd sandbox (01:30:53Z): A 0 %/100 %, B 0 %/87 %, C 3 %/18 % (5 h/weekly used).
- 2026-09-26: the logging half landed in #790. A probe that returns False writes one line
  to the journal (reason, seconds, whether the message went out, and the last 20 screen
  rows with emails and tokens redacted). An exception in `_refresh_usage` is logged with
  its traceback. What is left here is the throttle: skip a probe while the snapshot is
  younger than `UNCHANGED_REWRITE_SECONDS`, or count "unchanged" as success.
- 2026-09-26, the throttle half: `maybe_refresh_usage` reads the snapshot before anything
  else and returns without a probe while it is younger than `UNCHANGED_REWRITE_SECONDS`
  (imported from `statusline`), for the page, the button and a spent run alike. The one
  exception is `after_login`: a new account in the folder is probed whatever the age of the
  last account's snapshot. No change in `claude.py`: the boundary is clean, because a probe
  that starts after 60 s meets a recorder that will write. The reason is logged as a string
  in the journal line from #790, not returned as a code; nothing reads a code.
- The #810 runs tests gave their fake a snapshot "now", which this rule turns into "no
  probe"; they now use two minutes ago. The #790 tests that counted stderr lines flaked under
  parallel load: a probe started by an earlier test logged into the next one. They now keep
  only their own slot's lines (`_journal`).
- Verified: Windows `uv run pytest` on the ai_accounts tests, three runs; WSL 4 parallel x 5
  runs, 86 passed each time; ruff; mypy on `ai_accounts_agent` and the runs test.
