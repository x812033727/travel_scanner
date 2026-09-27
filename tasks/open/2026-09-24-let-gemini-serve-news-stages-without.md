---
id: 2026-09-24-let-gemini-serve-news-stages-without
title: Let Gemini serve news stages without collapsing block unions
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-24T00:27:41Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/ai/structured_output.py
  - apps/api/tests/test_structured_output.py
---

# Let Gemini serve news stages without collapsing block unions

## Why

`/admin/news` lets an administrator pick Gemini as the news writer or fact-checker, but
the Gemini adapter cannot return a news article. `gemini_response_schema` in
`apps/api/app/ai/structured_output.py` reduces a pydantic schema to Gemini's
`responseSchema` subset and, for every `anyOf`, keeps only the first non-null option. A
`GuideDocument`'s `blocks` is a union of thirteen block types (a `oneOf`, which the
converter does not handle at all, or an `anyOf` after
`app/news_automation/provider_schema.py`), so Gemini is told every block is a heading.
Pydantic then rejects the reply, the repair round trip fails the same way, and the
candidate fails.

Hotspot guides and the candidate generator use the same converter with schemas that have
no unions, so nothing is broken there today.

## Definition of done

- [ ] A Gemini news stage (draft, verification, translation, locale review) sends a
      schema that keeps every block type of a `GuideDocument`.
- [ ] The existing hotspot/guide schemas produce the same Gemini schema as before, or
      the change is shown harmless with a live 測試連線 on the admin AI cards.

## Steps

- [ ] Check whether Gemini's `responseSchema` accepts `anyOf` (or switch the news path to
      `responseJsonSchema`, which takes JSON Schema directly) against the production key.
- [ ] Keep unions in the converter, with a test on `LocalizedDocument.model_json_schema()`.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_structured_output.py tests/test_news_pipeline.py -q
```

## Notes

- Found while hardening the news automation (task
  2026-09-24-harden-hourly-news-automation-before-first). Until this lands, keep Gemini
  out of the news writer/checker settings; docs/news-automation.md says so.
