---
id: 2026-10-13-classify-failed-oauth-token-refresh-as
title: Classify Claude OAuth and organization subscription failures
status: done
priority: P2
area: api
owner: codex-open-task-reconcile-510e
claimed_at: 2026-10-24T13:13:29Z
created_at: 2026-10-13T08:05:42Z
completed_at: 2026-10-24T13:13:35Z
branch: codex/open-tasks-reconcile-20261024
depends_on: []
scope:
  - apps/api/ai_accounts_agent/runs.py
  - apps/api/tests/test_ai_accounts_agent_runs.py
---

# Classify Claude OAuth and organization subscription failures

## Why

AI account CLI failures containing the actual notice `Failed to refresh OAuth token` miss
`AUTH_MESSAGE` in `apps/api/ai_accounts_agent/runs.py`. The failed account then surfaces
as a generic `subscription_run_failed` (HTTP 502) instead of the existing
`subscription_auth_failed` response, which rests an account that needs sign-in.
The 2026-10-13 notice `Your organization has disabled Claude subscription access for
Claude Code` has the same 502 outcome but requires organization access to be enabled;
signing in the same account again alone may not help.

## Definition of done

- [x] A failed CLI result with the exact OAuth refresh notice rests that account for
  every model and returns `subscription_auth_failed` (HTTP 503), without a provider
  retry or exposing the CLI notice in the API response.
- [x] A successful answer quoting the notice remains a successful answer; unrelated
  failures keep their existing classification.
- [x] The exact organization-disabled notice rests only the failed slot, then permits
  the existing agent rotation to try the next signed-in slot. Its direct error detail
  directs the owner to organization access rather than another sign-in.

## Steps

- [x] Add a focused regression for the exact notice across the existing CLI output
  channels and one successful quoted answer.
- [x] Extend only the authentication notice matcher; run focused API checks.
- [x] Reproduce the organization-disabled notice in CLI output channels and agent
  rotation, then verify a successful answer quoting it stays successful.

## How to verify

`cd apps/api && uv run pytest tests/test_ai_accounts_agent_runs.py -q`
and `uv run ruff check ai_accounts_agent/runs.py tests/test_ai_accounts_agent_runs.py`.

## Notes

`AUTH_MESSAGE` already handles `OAuth token has expired`, but the observed wording
uses a different verb. This fix changes classification only; it must not trigger a
paid run or attempt a credential refresh.

2026-10-13 local result: Before the matcher change, the exact notice failed in all
four CLI output channels and direct classification (5 failures, 11 passing focused
cases). After the change, `tests/test_ai_accounts_agent_runs.py` has 60 passed;
Ruff and mypy for the touched code passed. `npm run check:tasks` passed with only
unrelated stale-claim warnings. No provider request or production retry was made.
Pending parent review and inclusion in draft PR #1480; not deployed.

2026-10-13 organization-disabled follow-up: Before the matcher change, six new cases
failed as expected (four failed CLI channels, direct classification, and agent
rotation). After the narrow matcher and organization-specific detail, all 66 focused
agent tests passed; Ruff and mypy for the two touched source files passed. The fake
CLI test moved from disabled slot `a` to signed-in slot `b` and marked only `a` as
resting. No real provider request or production retry was made. Pending parent review,
CI, and deployment in the same draft PR #1480.


### 2026-10-24 owner-directed reconciliation

站主要求處理全部open任務：不再需要或已有完成證據的項目結案。此為純任務紀錄接手；不接管其他live producer、不改產品scope檔、不發起付費、正式站寫入或YouTube操作。

Disposition: close_completed.

- PR #1480 MERGED 2026-10-18T20:30:54Z at 86c6d9bce117af85ce9267d408721c1f0f7c7dab with SUCCESS rollup.
- Fresh read-only current-main-based Windows validation: tests/test_ai_accounts_agent_runs.py plus tests/test_error_localization.py 69 passed, exit 0.

OAuth/organization故障分類的全部程式驗收已#1480落地，無任何provider測試呼叫需要再付費。
