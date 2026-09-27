---
id: 2026-09-27-news-evidence-excerpts-stop-at-8
title: News evidence excerpts stop at 8,000 characters, so the checks never see the rest of the page
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-27T09:42:28Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/scanner.py
  - apps/api/app/news_automation/validation.py
---

# News evidence excerpts stop at 8,000 characters, so the checks never see the rest of the page

## Why

The scanner stores each evidence page as `body_text[:8000]` / `linked_text[:8000]`
(`scanner.py`), and a refresh does the same (`validation.py`, `row.excerpt = article_text[:8000]`).
The writer, the fact check, the locale reviews and Jev all read only that excerpt. On
2026-09-27 an independent review of the 11 held news drafts found two published-quality
errors that came from the cut, not from the models:

- `ai-news-gemini-3-8-tts-20260923`: every locale's FAQ said Google "gave no availability
  details by region", and listed Gemini Enterprise as available. The post's closing rollout
  section, after the cut, says Enterprise API access is "coming soon". Its footnote also
  bars voice replication in Illinois, Texas, the EEA, the UK, Switzerland and India.
- `tech-news-github-css-modules-migration-20260925`: the draft's timeline stops at the May
  2026 sx-prop milestone. The post's last sections, after the cut, give the answer to the
  headline: github.com has run on 100% CSS Modules since June 2026.

A refresh cannot help either: it re-reads the page and truncates it at the same point.

## Definition of done

- [ ] A long official post's later sections reach the writer and the checks, either by storing
      more text or by storing the article body without the page's navigation and boilerplate.
      The model stages stay within their token budgets.
- [ ] A test with an evidence page longer than today's limit proves that a fact past the old
      cut-off is available to the fact check.

## Steps

- [ ] Measure the extracted text length of the last month's evidence pages, per source, to
      choose a limit or an extraction change.
- [ ] Change the scanner and `refresh_evidence` together, so that a refresh never shortens
      what the first scan stored.
- [ ] Check the prompts' input budgets (`ai.py` also cuts `excerpt[:6000]` for the duplicate
      check).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_automation.py tests/test_news_pipeline.py -q
```

## Notes

- Found in the 2026-09-27 review of the held drafts. The corrected drafts could only delete
  or soften the wrong statements, because the correct facts were not in the stored excerpts.
