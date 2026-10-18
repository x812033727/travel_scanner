---
id: 2026-10-11-a-news-candidate-whose-slug-is
title: A news candidate whose slug is already used is recorded as failed
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-11T05:23:54Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/pipeline.py
  - apps/api/tests/test_news_pipeline.py
  - docs/news-automation.md
---

# A news candidate whose slug is already used is recorded as failed

## Why

When a candidate reaches publication and its article slug is already taken, the pipeline
raises `AppError(409, "news_slug_conflict")` (`apps/api/app/news_automation/pipeline.py`)
and the candidate ends as `failed` with `error_code = AppError`.

Seen on 2026-10-11 02:42Z: after the source list was reloaded, "Anthropic news" filed
`https://www.anthropic.com/claude-sonnet-5-5` again and it went through the model stages
before stopping there. The site already had that story, so not publishing was right. But
`failed` puts it in the 需重寫 list beside real failures, where 重新執行 would spend
model calls on a story that is already published, and the error code names the exception
class instead of the reason.

## Definition of done

- [ ] A slug conflict with a published article of the same story ends the candidate as a
      duplicate of that article (or with its own error code), not as `failed` / `AppError`.
- [ ] It is caught before the paid stages when the slug can be known then; if it cannot,
      that is written here.
- [ ] `docs/news-automation.md` names the outcome.

## Steps

- [ ] Find where the slug is derived and whether the scanner's duplicate checks (URL,
      normalized title, body hash) could have matched this candidate to the earlier one:
      the earlier candidate may predate the body hash, or the page title may have changed.
- [ ] Decide the status: `duplicate` pointing at the article, or `rejected` with
      `news_slug_conflict`.
- [ ] A test in `apps/api/tests/test_news_pipeline.py`.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_pipeline.py -q
```

## Notes

- One occurrence so far. Loading many sources at once makes it likelier, because a first
  scan of a re-keyed source can file pages the site already covered through another row.
