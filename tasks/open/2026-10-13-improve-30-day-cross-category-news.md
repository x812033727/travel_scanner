---
id: 2026-10-13-improve-30-day-cross-category-news
title: Improve 30-day cross-category news duplicate recall beyond newest-row cap
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-13T04:58:34Z
completed_at:
branch:
depends_on:
  - 2026-10-13-detect-duplicate-hourly-news-events-across
scope:
  - apps/api/app/news_automation/duplicates.py
  - apps/api/tests/test_news_pipeline.py
  - docs/news-automation.md
---

# Improve 30-day cross-category news duplicate recall beyond newest-row cap

## Why

The cross-category duplicate screen introduced in the related task reads at most
160 recent published guide-search rows before matching event cues. A same-event
article can still be within the 30-day duplicate window but fall outside that
newest-row cap when many newer articles and locales have been published. That
article would then be absent from the AI judge's known-story context.

## Definition of done

- [ ] A published same-event article in another category remains discoverable
  throughout the 30-day duplicate window even when more than 160 newer rows
  exist, without unbounded database reads or AI judge context.
- [ ] The existing different-event and later-development exclusions still hold.

## Steps

- [ ] Design an indexed or prefiltered retrieval path that finds likely event
  matches before applying a bounded result cap.
- [ ] Add a regression with more than 80 newer two-locale articles preceding
  an older same-event match, plus distinct-event controls.
- [ ] Document the query bound and retained judge-context limit.

## How to verify

Run `uv run pytest tests/test_news_pipeline.py -q` from `apps/api`, then
`uv run ruff check app/news_automation/duplicates.py tests/test_news_pipeline.py`
and `uv run mypy app/news_automation/duplicates.py tests/test_news_pipeline.py`.

## Notes

The current cap is deliberate to keep a small one-call AI judge budget and
avoid loading the full news catalog. This ticket follows the cross-category
duplicate guard; it is not grounds to remove that guard or auto-reject a match.
