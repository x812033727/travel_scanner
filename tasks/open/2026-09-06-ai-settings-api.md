---
id: 2026-09-06-ai-settings-api
title: Consolidate AI vendor keys, model catalog and per-feature models (API)
status: in-progress
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T06:23:36Z
created_at: 2026-09-06T06:23:04Z
completed_at:
branch: claude/ai-settings-consolidation
depends_on: []
scope:
  - apps/api/app/admin/service.py
  - apps/api/app/admin/schemas.py
  - apps/api/app/ai/catalog.py
  - apps/api/app/config.py
  - apps/api/app/hotspots/ai_search.py
  - apps/api/app/hotspots/admin_router.py
  - apps/api/migrations/versions/0047_ai_vendor_settings.py
  - apps/api/tests
  - .env.example
  - README.md
---

# Consolidate AI vendor keys, model catalog and per-feature models (API)

## Why

The admin provider definitions kept the OpenAI, Claude and MiniMax keys (and Base URLs)
on the `ai_planner` row and the Gemini key on the `gemini_guides` row, while
`ai_guide_search` had no key fields at all and borrowed the planner's. Disabling the
planner therefore nulled every AI key, including the ones guide search needs. Model ids
were free text with no validation, even though the Gemini id is interpolated into the
request path (security audit R2-25), and there was no way to run guide search on a
different model than the planner.

## Definition of done

- [x] One provider, `ai_vendors`, owns the four API keys and the four official Base URLs;
      it is never disabled and its secrets are never nulled.
- [x] `ai_planner` and `ai_guide_search` each choose vendor + model; guide search may
      override the planner's model per vendor, empty means "same as the planner".
- [x] The snapshot exposes server-curated model options per model field
      (`field_options`), and every stored model id must match
      `^[A-Za-z0-9._:-]{1,128}$` (catalog id or custom).
- [x] Existing encrypted keys move automatically (migration 0047); nothing has to be
      re-entered.

## Steps

- [x] `apps/api/app/ai/catalog.py`: vendor catalog, `MODEL_FIELDS`, validation helper.
- [x] `config.py`: `hotspot_guide_ai_{openai,anthropic,minimax}_model` (optional).
- [x] `admin/service.py`: `ai_vendors` definition, `ALWAYS_ENABLED_PROVIDERS`, model id
      validation, `field_options` in the snapshot, legacy-row warning, `ai_vendors`
      status and connection test (`_test_ai_vendors`), `hotspot_guides` status branch,
      vendor-secret redaction for the feature tests.
- [x] `hotspots/ai_search.py`: `research_model` resolves override → planner model;
      `ai_search_overview` for the admin dialog.
- [x] `hotspots/admin_router.py`: run provider defaults to the configured default;
      coverage returns `models` per vendor.
- [x] Migration `0047_ai_vendor_settings` (Python data move, idempotent, downgrade).
- [x] Tests, `.env.example`, README.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest
RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_migration_0047_ai_vendors.py   # needs PostgreSQL
```

After deploy: `select provider, config::text from provider_configs where provider in
('ai_vendors','ai_planner','gemini_guides')` shows the Base URLs on `ai_vendors` only, and
`/admin/settings` → AI 服務 → each card's 測試連線 succeeds.

## Notes

- Rollback caveat: the deploy script never runs `alembic downgrade`; rolled-back code
  does not read `ai_vendors`, so the keys vanish until `alembic downgrade 0046` runs in
  the old release or the keys are re-entered.
- Behaviour change on purpose: disabling `ai_planner` no longer clears the vendor keys;
  `ai_planner_enabled=False` still stops the planner and the trip parser.
- MiniMax documents no models-list endpoint, so `_test_ai_vendors` treats its 404/405 as
  "configured, not verified"; OpenAI, Claude and Gemini are verified by listing models.
- Model ids in the catalog: OpenAI (`gpt-6-astra`, `gpt-5.6-sol`, `gpt-5.6-terra`,
  `gpt-5.6-luna`) and MiniMax (`MiniMax-M3`, `M2.7`, `M2.7-highspeed`, `M2.5`) were read
  from the vendors' model pages on 2026-09-06; Gemini from Google's page the same day.
  `test_ai_catalog.py` pins the four Settings defaults to the catalog.
- `provider_configs.config` is `json`, not `jsonb`; the migration binds dicts through
  `sa.JSON` and `test_migration_sql_dialect.py` now guards that table too.
- The migration must not use `from __future__ import annotations`: the tests load it with
  `importlib` outside `sys.modules`, and dataclasses then cannot resolve string
  annotations.
