---
id: 2026-09-24-let-gemini-serve-news-stages-without
title: Let Gemini serve news stages without collapsing block unions
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-gemini-unions
claimed_at: 2026-10-02T15:23:58Z
created_at: 2026-09-24T00:27:41Z
completed_at:
branch: claude/gemini-structured-unions
depends_on: []
scope:
  - apps/api/app/ai/structured_output.py
  - apps/api/tests/test_structured_output.py
  - docs/news-automation.md
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

- [x] A Gemini news stage (draft, verification, translation, locale review) sends a
      schema that keeps every block type of a `GuideDocument`.
- [x] The existing hotspot/guide schemas produce the same Gemini schema as before, or
      the change is shown harmless with a live 測試連線 on the admin AI cards.

## Steps

- [ ] Check whether Gemini's `responseSchema` accepts `anyOf` (or switch the news path to
      `responseJsonSchema`, which takes JSON Schema directly) against the production key.
      Checked against the documentation only (no real model calls in this task); the
      live check moved to task 2026-10-02-confirm-a-live-gemini-news-stage.
- [x] Keep unions in the converter, with a test on `LocalizedDocument.model_json_schema()`.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_structured_output.py tests/test_news_pipeline.py -q
```

## Notes

- Found while hardening the news automation (task
  2026-09-24-harden-hourly-news-automation-before-first). Until this lands, keep Gemini
  out of the news writer/checker settings; docs/news-automation.md says so.
- 2026-10-02 (claude-opus-5-5-gemini-unions). What the converter did: the news replies
  are `ProviderReply` models, so their schema is already `portable_json_schema` (the
  block union is an `anyOf` of 13 `$ref`s, inlines an `anyOf` of 4); the old `anyOf`
  branch kept option 0, so `blocks.items` became a lone HeadingBlock. A raw pydantic
  `oneOf` (with `discriminator`) fell through to the scalar branch and became `{}`.
- Decision: keep the converter and `responseSchema` rather than switching the news path
  to `responseJsonSchema` (that would change `app/ai/gemini.py` and every Gemini caller).
  A union with two or more non-null options now becomes `{"anyOf": [...]}` (plus
  `nullable`/`description`); `oneOf` is read the same way; the discriminator is dropped,
  but every option keeps its one-value `type` enum and pydantic enforces the
  discriminator on the reply. A one-option union is converted exactly as before.
  Gemini's `Schema` gained `anyOf` in March 2025 (Google staff on
  discuss.ai.google.dev, thread "oneOf in response_schema").
- Second blocker found on the way: `HeadingBlock.level` (`Literal[2, 3]`) became
  `{"type": "integer", "enum": ["2", "3"]}`. The Gemini API documents `enum` as "values
  of the element of Type.STRING", and other clients report a 400 for numeric enums. A
  non-string enum now keeps its type and moves its values into the description ("One
  of: 2, 3."). No schema outside the news replies has a non-string enum.
- Verified byte-identity with a scratch script that posted every (provider, model) pair
  through the real adapters into an httpx.MockTransport, on origin/main and on the
  branch: 112 digests (16 models x Gemini schema, model_json_schema,
  schema_instructions and the request body of openai/minimax/anthropic/gemini), and only
  the 8 Gemini entries of the 4 news replies changed. In the tests,
  `test_gemini_schemas_without_unions_are_byte_identical_to_before` freezes the old
  converter and compares all 12 non-news models against it, and
  `test_other_providers_still_receive_the_news_schema_unchanged` checks the schema
  OpenAI, MiniMax and Claude receive. The new Gemini news schemas are about 12 KB.
- Scope: added docs/news-automation.md, whose "Known limits" bullet described the old
  converter. The two review-state tickets that also list it
  (2026-09-30-microsoft-official-blog-and-the-block,
  2026-09-30-news-automation-has-no-taiwan-sources) belong to PR #1041, already merged.
- Not done: no request reached the Gemini API. The settings CLI keeps refusing Gemini
  (its comment still gives the old reason) until task
  2026-10-02-confirm-a-live-gemini-news-stage records a live stage. Choosing Gemini on
  /admin/news is the owner's setting decision.
