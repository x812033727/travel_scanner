---
id: 2026-10-21-guard-october-brand-story-batch-with
title: Guard October brand story batch with USD 25 film accounts
status: blocked
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-21T00:17:11Z
completed_at:
branch: codex/brand-stories-20261020
depends_on: []
scope:
  - apps/api/app/video_budget/models.py
  - apps/api/app/video_budget/service.py
  - apps/api/app/video_automation/ai.py
  - apps/api/migrations/versions/0137_brand_story_batch_budget.py
  - apps/api/tests/test_video_pilot_budget.py
  - apps/api/tests/test_video_automation_ai.py
  - apps/api/tests/test_migration_0137_brand_story_batch_budget.py
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
  - apps/api/tests/test_video_media_api.py
  - apps/api/app/video_media/admin_api.py
  - apps/api/tests/test_story_budget_rollback_integration.py
  - apps/api/tests/test_video_story_policy.py
  - tasks/open/2026-10-21-guard-october-brand-story-batch-with.md
---

# Guard October brand story batch with USD 25 film accounts

## Why

The five new `story-new-20261020-*` films are not in the existing durable all-in budget registry. Importing this hands-off series can start paid writing, speech, image, judge and music work while the generic media setting allows up to US$200 and does not include text or speech. The owner fixed each brand story's complete-film ceiling at US$25. Register only these five slugs with independent accounts before any production import.

## Definition of done

- [x] Each of the five exact new slugs has a durable US$25 film account; missing or wrong-limit accounts block paid dispatch.
- [x] The client uses durable request receipts for every paid writing/checking stage, even if the site's generic durable flag is off.
- [x] Existing pilot and US$5 follow-on limits, slugs and media behavior remain unchanged.

## Steps

- [x] Add the five slugs to the API budget registry and the client's durable set.
- [x] Add an idempotent additive migration after revision 0136; preserve all accounts and receipts on rollback.
- [x] Run focused account/dispatch, migration and client tests, then document the remaining live price and total-cost preflight.

## How to verify

`cd apps/api && uv run pytest tests/test_video_pilot_budget.py tests/test_migration_0137_brand_story_batch_budget.py -q && uv run ruff check app/video_budget/models.py migrations/versions/0137_brand_story_batch_budget.py tests/test_video_pilot_budget.py tests/test_migration_0137_brand_story_batch_budget.py`; from root run `node --test tools/video/automation/client.test.mjs` and `npm run check:tasks`. Live payment remains stopped until the site is reachable, the migration and worker are deployed, and a full batch cost quote is reviewed.

## Notes

The existing `PILOT_SLUGS` registry (API) and `PILOT_STORY_SLUGS` (client) omitted all five new episode slugs. `video_automation/models.py` defaults `max_usd_per_video` to 200 and `tools/video/media/stages.mjs` applies it only to media ledger. This task extends the existing cross-route US$25 pilot service without changing that global setting. The new series has not been imported or paid for.

The `story-new-20261020-` prefix also guards later episodes: a future slug must get its own US$25 account before import, or paid dispatch fails closed. The subscription writer/checker path checks account validity before model selection because that path records durable jobs without a USD reservation. Each later batch needs a reviewed account-seeding migration; the current migration creates only the first five accounts.

Focused API tests passed (75 passed, 3 integration skips); speech, media-job/judge and subscription regression tests passed (110 passed). Client tests passed (43). Ruff, Mypy, Alembic head, task validation and `git diff --check` passed. Live provider pricing and the full-batch estimate still need review before the worker spends; no migration or video import was run against production.

Blocked handoff (2026-10-21): the implementation is ready for integration, but PR creation and deployment are blocked by API/network access in this environment. Resume by reviewing the change, confirming the live price quote, committing and opening the PR, then deploying revision 0137 before importing or running these episodes. No production API call or vendor spend was made for this batch.
