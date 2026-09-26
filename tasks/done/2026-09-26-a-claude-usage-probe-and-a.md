---
id: 2026-09-26-a-claude-usage-probe-and-a
title: A Claude usage probe and a prompt run never share an account at once
status: done
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-26T05:22:11Z
created_at: 2026-09-26T05:22:04Z
completed_at: 2026-09-26T13:20:50Z
branch: claude/ai-accounts-probe-run-lock-2
depends_on: []
scope:
  - apps/api/ai_accounts_agent/server.py
  - apps/api/tests/test_ai_accounts_agent_runs.py
  - apps/api/tests/test_ai_accounts_antigravity.py
  - ops/ai-accounts/README.md
  - tasks/open/2026-09-25-skip-claude-usage-probes-the-recorder.md
---

# A Claude usage probe and a prompt run never share an account at once

## Why

On 2026-09-26 at 04:36 UTC claude-b's usage probe returned False, and in the same minute the
news draft's `/v1/runs` call on B failed twice (news_pipeline_runs 04:36:10 and 04:36:24):
`subscription_run_failed: claude run failed: Failed to refresh OAuth token ... Claude Code
process is refreshing it or exited mid-refresh`. current-claude was c and default-claude b;
C was busy, so the run went to B while the page-triggered probe was running there. Two CLIs
on one account refreshed its OAuth token at once. `maybe_refresh_usage` never looked at
`_runs_busy`, and `_claim_run_slot` never looked at `_usage_running`.

## Definition of done

- [x] No Claude usage probe starts on a slot with a run; the next page view or the run's
      end probes it.
- [x] A run passes over a slot being probed. When it is that slot's turn, it waits for the
      probe (within `queue_seconds`) instead of spending another account, and the turn
      does not pass on because of a probe.
- [x] A probe's end wakes runs waiting for its account.

## Steps

- [x] `server.py`: one lock order (`_runs_changed`, then `_usage_lock`); the checks above.
- [x] Tests in `test_ai_accounts_agent_runs.py`.
- [x] README: "Prompt runs" says a probe counts as a run.
- [x] Fix the Antigravity login test's race that failed #790's CI once.

## How to verify

`cd apps/api && uv run pytest tests/test_ai_accounts_agent_runs.py tests/test_ai_accounts_agent.py`;
the POSIX ones in WSL (skill dev-and-ci). On the host, after the agent is reinstalled, a news
run and a page's probe on one account no longer overlap.

## Notes

- The run's own `overview(False)` starts probes on stale slots. The first draft treated a
  probed current slot like a busy one, so the run went to the next account, which breaks
  "A until full". Under parallel load `test_the_turn_survives_a_restart_and_the_default_restarts_it`
  caught it. Now `_claim_run_slot` picks again, ignoring probes; if that answer is the
  current slot, it waits.
- `test_page_login_picks_google_takes_the_code_and_reads_the_quota` flaked in #790's CI and
  in WSL. Usage is read fresh, but email and plan come through the status cache, which the
  probe clears only when it ends. The test now waits for `usage_refreshing` to go false.
  Under 4 parallel WSL runs x 5: 20/20 passed, where before about 1 in 15 failed.
- Verified: Windows `uv run pytest` on the ai_accounts tests; WSL 85 passed, 8 runs in a
  row plus the parallel stress; ruff; mypy on `ai_accounts_agent` and the runs test.
- The older ticket `2026-09-25-skip-claude-usage-probes-the-recorder` also asked for failure
  logging; #790 did that, and its notes now say so. Its other half (the recorder's 60 s
  throttle reading as a failed probe) is still open.
