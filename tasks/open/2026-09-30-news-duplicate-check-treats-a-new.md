---
id: 2026-09-30-news-duplicate-check-treats-a-new
title: News duplicate check treats a new model version as a duplicate of the previous one
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-30T10:34:33Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/duplicates.py
  - apps/api/tests/test_news_pipeline.py
---

# News duplicate check treats a new model version as a duplicate of the previous one

## Why

Jev's duplicate check compares a story with the same category's news of the last 30 days.
A new version of a model family (GPT-6.1 Sol a week after GPT-6 Sol) shares the name and
most of the vocabulary with the article about the previous version, so it is likely to be
judged a duplicate or "uncertain" and wait in manual review. Not yet observed on the host
(the GPT-6.1 Sol candidate never existed, see the scanner task), so measure first. Found 2026-09-30 while writing batch 4.9 by hand (`tasks/open/2026-09-30-news-batch-4-9-gpt-6.md`).

## Definition of done

- [ ] The duplicate prompt states that a new version, a new model in a family, or a price
      change announced later is a new event, and a regression test holds a pair like
      "GPT-6 Sol and Luna launch" / "GPT-6.1 Sol launch" as not duplicate.
- [ ] Look up on the host how many `news_duplicate_uncertain` holds of the last 30 days were
      new versions; write the number here.

## How to verify

`cd apps/api && uv run pytest tests/test_news_pipeline.py -q`
