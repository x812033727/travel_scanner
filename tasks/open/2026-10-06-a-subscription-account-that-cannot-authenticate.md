---
id: 2026-10-06-a-subscription-account-that-cannot-authenticate
title: A subscription account that cannot authenticate rests and the stage job fails instead of turning uncertain
status: review
priority: P1
area: api
owner: claude-fable-5-1-video-unstuck
claimed_at: 2026-10-06T05:57:31Z
created_at: 2026-10-06T05:57:11Z
completed_at:
branch: claude/video-unstuck-subscription-auth
depends_on: []
scope:
  - apps/api/ai_accounts_agent/runs.py
  - apps/api/ai_accounts_agent/server.py
  - apps/api/app/video_automation/subscription.py
  - apps/api/app/video_automation/ai.py
  - apps/api/app/ai/subscription.py
  - apps/api/app/admin_ai_accounts/agent.py
  - apps/api/tests/test_ai_accounts_agent_runs.py
  - apps/api/tests/test_video_automation_subscription.py
  - apps/api/tests/test_video_automation_ai.py
  - apps/api/tests/test_ai_subscription.py
  - ops/ai-accounts/README.md
---

# A subscription account that cannot authenticate rests and the stage job fails instead of turning uncertain

## Why

On 2026-10-06 the production video `cloudflare-auto-router-who-measured-savings` was
blocked with "writer may have run on the server without its answer reaching the worker
(訂閱帳號執行失敗：claude run failed: Failed to authenticate. API Error: 403 Access to this
model requires an access grant your request does not have.)". The stage job row was
`uncertain` with `video_ai_upstream_failed`, so the worker would not ask again until the
owner retried by hand, although no model had run at all.

The chain: `ai_accounts_agent/runs.py` raised `CliError("claude run failed: …")` for every
failure that was not a usage limit (only `LIMIT_MESSAGE` rested an account and moved on);
`app/video_automation/subscription.py` mapped it to 502 `video_ai_upstream_failed`;
`NO_MODEL_CALL_ERRORS` in `app/video_automation/ai.py` did not list it, so
`run_jobs._mark_error` marked the job `uncertain`.

## Definition of done

- [x] A failed CLI run whose short notice says the account cannot authenticate ("Failed to
      authenticate", "API Error: 401/403", "requires an access grant", "not logged in", an
      expired OAuth token, "invalid api key") is a `RunRefused` 503 `subscription_auth_failed`
      for every model family, on Claude and on Codex; a long successful answer that merely
      quotes such words is still an answer.
- [x] The agent rests that account for 30 minutes, moves on to the next signed-in one, and
      forces no usage probe on it. When every signed-in account rests for this reason the
      answer is 503 `subscription_auth_failed` ("sign one in again"), not
      `subscription_quota_paused`; one account at its limit plus one signed out is still a
      usage pause.
- [x] A video stage sees 503 `video_ai_subscription_auth_failed` with `retry_after` 900,
      writes no `VideoAiRun` row, and a durable job ends `failed` (the worker asks again)
      rather than `uncertain`.
- [x] News and guide features treat `subscription_auth_failed` as a wait (`WAIT_CODES`).

## Steps

- [x] `runs.py`: `AUTH_MESSAGE`, `auth_refusal`, `auth_failed_everywhere`; applied on the
      failed path of `run_claude` (after the outdated-CLI check, before the limit check) and
      of `run_codex`.
- [x] `server.py`: `_auth_failed[(tool, slot)] = until`; `_release_run_slot(auth_failed=)`
      skips the forced probe; `_claim_run_slot` turns a `subscription_quota_paused` from
      `pick_slot` into `subscription_auth_failed` when every usable account is auth-resting.
- [x] `video_automation/subscription.py` mapping; `ai.py` `NO_MODEL_CALL_ERRORS` and
      `SUBSCRIPTION_RAN_NOTHING`; `app/ai/subscription.py` `WAIT_CODES`; `agent.py`
      docstring; `ops/ai-accounts/README.md` next to the 30-minute limit rule.
- [x] Tests in the four test files.

## How to verify

```bash
cd apps/api
PYTHONUTF8=1 uv run pytest tests/test_ai_accounts_agent_runs.py tests/test_ai_accounts_agent*.py \
  tests/test_video_automation_subscription.py tests/test_video_automation_ai.py \
  tests/test_video_stage_jobs.py tests/test_ai_subscription.py tests/test_error_localization.py
uv run ruff check . && uv run mypy app && uv run mypy tests
```

On the host after deploy: with claude-a still returning the 403, a writer stage run should
land on claude-b; the agent log shows no forced probe of a; if every account fails, the
stage job row reads `failed` / `video_ai_subscription_auth_failed` with `retry_after`, and
the worker asks again after 15 minutes. The account is not signed out by the agent: the AI
accounts page still shows it signed in, and the owner signs it in again there.

## Notes

- The tools side (`tools/video/automation/client.mjs` `PAUSE_CODES`) must learn
  `video_ai_subscription_auth_failed` so the worker treats it like a pause; a sibling PR owns
  that file, so it is not in this task's scope.
- `.agents/skills/prod-host-ops/references/ai-accounts.md` (mirrored under
  `.claude/skills/`) still describes only the usage-limit rest; it is outside this scope and
  could take one line about the auth rest.
- No admin page renders the agent's refusal codes as sentences (the codes appear only in
  Python), so no four-language `ERROR_DETAILS` entries were needed;
  `test_error_localization.py` scans literal `AppError(` calls only.
- `auth_refusal` reads only a failed run's short notice (`LIMIT_NOTICE_CHARS`), stderr, and a
  short bare stdout (when the CLI printed no JSON at all); a successful answer is never read.
- The forced usage probe is skipped on an auth rest because the probe runs the same CLI on
  the same account and would fail the same way (and would count as a run on the account).
- The blocked production video still needs its stage job retried once this is deployed; the
  fix only changes what happens to the next such failure.
