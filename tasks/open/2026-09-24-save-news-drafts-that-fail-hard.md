---
id: 2026-09-24-save-news-drafts-that-fail-hard
title: Save news drafts that fail hard checks as editable articles
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-24T11:21:15Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/pipeline.py
  - apps/api/tests/test_news_pipeline.py
---

# Save news drafts that fail hard checks as editable articles

## Why

`process_candidate` saves the five-locale guide article only after the hard checks pass
(`apps/api/app/news_automation/pipeline.py`, `_save_guide_bundle` after
`hard_policy_problems`). A draft that fails them (a missing FAQ block, a missing topic
link, a forbidden word in one locale) is kept only in `draft_bundle_json`: the admin page
shows it and its lint, but there is no article to open in the guide editor, so a small
formatting problem costs a whole new draft. Since 2026-09-24 these candidates go to the
需重寫 list with only 重新執行 and 退件.

## Definition of done

- [ ] A hard-check failure saves the bundle as an unpublished guide article, so the
      candidate goes to manual review with the editor links, and 重新查核 re-runs the
      checks on the edited drafts.
- [ ] Nothing about publication changes: publish still needs every check to pass.

## Steps

- [ ] Save the bundle before returning the hard-check hold; `_needs_redraft` then keeps
      it in manual review because it has an article.
- [ ] Pipeline test for both paths.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_pipeline.py tests/test_news_review_actions.py -q
```

## Notes

- Found while making the review queue actionable
  (task 2026-09-24-make-the-news-review-queue-actionable). Measure first: on 2026-09-24
  hard-check failures were rare next to fact-check and locale-review stops.
