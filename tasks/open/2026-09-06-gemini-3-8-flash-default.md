---
id: 2026-09-06-gemini-3-8-flash-default
title: Default the Gemini guide model to gemini-3.8-flash
status: in-progress
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T03:41:42Z
created_at: 2026-09-06T03:41:40Z
completed_at:
branch: claude/gemini-3-8-flash
depends_on: []
scope:
  - apps/api/app/config.py
  - .env.example
---

# Default the Gemini guide model to gemini-3.8-flash

## Why

The Gemini provider (guide article search through Google Search grounding, and the
hotspot candidate generator) shipped with `gemini-3.5-flash` as its default, while
`.env.example` still pointed at `gemini-2.5-pro` and told operators that Flash-tier
models are unusable. Production is moving to `gemini-3.8-flash` on 2026-09-06 through the
admin provider settings, so the shipped default and the env example should say the
same thing as the running site.

## Definition of done

- [x] A fresh install with no admin override calls `gemini-3.8-flash`.
- [x] `.env.example` no longer recommends a model that is closed to new keys.

## Steps

- [x] Change the default of `hotspot_guide_gemini_model` in `apps/api/app/config.py`.
- [x] Update `HOTSPOT_GUIDE_GEMINI_MODEL` and its comment in `.env.example`.

## How to verify

```bash
cd apps/api && uv run ruff check app/config.py && uv run pytest tests/test_hotspot_gemini_guides.py tests/test_hotspot_candidate_generation.py -q
```

On production, open `/admin/settings`, pick 景點內容 then Gemini 多語文章搜尋, and run
測試連線: it should report success and name `gemini-3.8-flash`.

## Notes

- The production `provider_configs` row for `gemini_guides` stores
  `hotspot_guide_gemini_model` explicitly, so changing the code default alone changes
  nothing on the site; the admin `PUT /admin/provider-settings/gemini_guides` does.
- Google lists `gemini-3.8-flash` as a stable model (ai.google.dev/gemini-api/docs/models,
  read 2026-09-06). `gemini-2.5-pro` returns 404 for new keys.
- The admin help text for this field is its own task: 2026-09-06-stale-gemini-model-help.
- As of this commit the production row still holds gemini-3.5-flash: the automated psql
  update was not permitted in this session, so the operator sets the value in /admin/settings
  (景點內容 → Gemini 多語文章搜尋 → Gemini 模型) and then runs 測試連線.
