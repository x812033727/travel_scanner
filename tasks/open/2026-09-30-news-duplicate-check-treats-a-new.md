---
id: 2026-09-30-news-duplicate-check-treats-a-new
title: News duplicate check treats a new model version as a duplicate of the previous one
status: review
priority: P2
area: api
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T12:13:26Z
created_at: 2026-09-30T10:34:33Z
completed_at:
branch: claude/gifted-rubin-umw5s4
depends_on: []
scope:
  - apps/api/app/news_automation/duplicates.py
  - apps/api/app/news_automation/ai.py
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

- [x] The duplicate prompt states that a new version, a new model in a family, or a price
      change announced later is a new event, and a regression test holds a pair like
      "GPT-6 Sol and Luna launch" / "GPT-6.1 Sol launch" as not duplicate.
- [ ] Look up on the host how many `news_duplicate_uncertain` holds of the last 30 days were
      new versions; write the number here.

## How to verify

`cd apps/api && uv run pytest tests/test_news_pipeline.py -q`

## Notes

- 2026-09-30: the question lives in `ai.jev_duplicate_check`, not `duplicates.py`. Its
  instructions now say a new version or successor, a new model in a family and a later
  price, availability or region change are new developments, with the GPT-6.1 Sol / Sonnet
  5.5 pairs as examples. Jev cannot run in tests, so the test pins the question it is sent
  (`test_duplicate_question_tells_jev_a_new_model_version_is_a_new_event`).
- Left: the host count of `news_duplicate_uncertain` holds of the last 30 days that were new
  versions (needs the host database).
