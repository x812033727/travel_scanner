---
id: 2026-10-13-classify-failed-oauth-token-refresh-as
title: Classify failed OAuth token refresh as subscription authentication failure
status: review
priority: P2
area: api
owner: codex-news-hourly-backlog-oauth
claimed_at: 2026-10-13T08:05:46Z
created_at: 2026-10-13T08:05:42Z
completed_at:
branch: codex/news-hourly-review-20261013
depends_on: []
scope:
  - apps/api/ai_accounts_agent/runs.py
  - apps/api/tests/test_ai_accounts_agent_runs.py
---

# Classify failed OAuth token refresh as subscription authentication failure

## Why

AI account CLI failures containing the actual notice `Failed to refresh OAuth token` miss
`AUTH_MESSAGE` in `apps/api/ai_accounts_agent/runs.py`. The failed account then surfaces
as a generic `subscription_run_failed` (HTTP 502) instead of the existing
`subscription_auth_failed` response, which rests an account that needs sign-in.

## Definition of done

- [x] A failed CLI result with the exact OAuth refresh notice rests that account for
  every model and returns `subscription_auth_failed` (HTTP 503), without a provider
  retry or exposing the CLI notice in the API response.
- [x] A successful answer quoting the notice remains a successful answer; unrelated
  failures keep their existing classification.

## Steps

- [x] Add a focused regression for the exact notice across the existing CLI output
  channels and one successful quoted answer.
- [x] Extend only the authentication notice matcher; run focused API checks.

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
