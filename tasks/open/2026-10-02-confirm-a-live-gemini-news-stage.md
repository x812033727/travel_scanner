---
id: 2026-10-02-confirm-a-live-gemini-news-stage
title: Confirm a live Gemini news stage before the settings CLI accepts Gemini
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-02T15:42:30Z
completed_at:
branch:
depends_on:
  - 2026-09-24-let-gemini-serve-news-stages-without
scope:
  - apps/api/app/news_automation/settings_cli.py
  - apps/api/tests/test_news_settings_cli.py
  - docs/news-automation.md
---

# Confirm a live Gemini news stage before the settings CLI accepts Gemini

## Why

Task 2026-09-24-let-gemini-serve-news-stages-without made `gemini_response_schema` keep
every option of a union, so a Gemini news stage now sends all 13 `GuideDocument` block
types (as an `anyOf`) instead of telling Gemini that every block is a heading, and a
heading's `level` no longer carries an enum on an integer. That was verified only with
fake transports: no request reached the Gemini API, because that ticket allowed no real
model calls.

Two things are still unproven against the production key: that `responseSchema` accepts
this `anyOf` (Google added `anyOf` to the Gemini API `Schema` in March 2025), and that a
schema of about 12 KB with 13 inlined block types stays under Gemini's complexity limit
("very large or deeply nested schemas may be rejected"). Until then the host's
`python -m app.news_automation.settings_cli` still refuses Gemini as writer, verifier or
editor (`UNSUPPORTED_FOR_NEWS`), and its comment and docstring still give the old reason.
/admin/news itself never refused Gemini.

## Definition of done

- [ ] One Gemini news stage (draft or translation) has run against the production key
      and returned a `GuideDocument` that validates, or the exact API error is recorded
      here.
- [ ] If it validated: the settings CLI accepts Gemini, its comment and docstring and
      `docs/news-automation.md` (step 4 and "Known limits") say so, and
      `tests/test_news_settings_cli.py` covers it. If it failed: the error and the next
      fix (for example `responseJsonSchema`) are written down here.

## Steps

- [ ] With the owner's agreement, run one stage with Gemini as the provider (an admin
      測試連線 card or a single candidate), and keep the request's schema size and the
      response status.
- [ ] Remove `gemini` from `UNSUPPORTED_FOR_NEWS` only after a valid reply.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_settings_cli.py tests/test_structured_output.py -q
```

## Notes

- Choosing Gemini for a news stage on /admin/news is the owner's setting decision; this
  ticket only removes the CLI's refusal once the API is shown to accept the schema.
