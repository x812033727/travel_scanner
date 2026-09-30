---
id: 2026-09-30-news-scanner-keeps-a-refused-article
title: News scanner keeps a refused article page as a feed-summary lead instead of skipping it forever
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T10:35:30Z
created_at: 2026-09-30T10:34:32Z
completed_at:
branch: claude/gifted-rubin-umw5s4
depends_on: []
scope:
  - apps/api/app/news_automation/scanner.py
  - apps/api/tests/test_news_automation.py
  - apps/web/lib/admin-news-messages
  - docs/news-automation.md
---

# News scanner keeps a refused article page as a feed-summary lead instead of skipping it forever

## Why

OpenAI published about seven stories on its RSS feed on 2026-09-28/29 (GPT-6.1 Sol, the
DevDay recap, dots, ...) and the hourly automation published none of them, while it
published 20 AI stories from other sites after 9/24. `openai.com/index/*` answers the
scanner with HTTP 403 (a Cloudflare "Enable JavaScript and cookies" page, about 9.8 KB).
`scan_source` treats a failed article fetch as a skip, reports it in `last_error` and tries
again next hour, forever: no candidate is ever stored, so nobody sees the story in
`/admin/news`. Found 2026-09-30 while writing batch 4.9 by hand (`tasks/open/2026-09-30-news-batch-4-9-gpt-6.md`).

## Definition of done

- [ ] An entry whose article page is refused (401/403), published in the last 72 hours and
      carrying a feed summary becomes a candidate in `needs_evidence` with the summary as its
      only `lead_only` evidence and error code `news_page_refused`. No model call is made and
      nothing can publish from it.
- [ ] Transient failures (timeouts, 429, 5xx) and entries without a summary or older than 72
      hours are still skipped and retried as before.
- [ ] The admin queue names the new hold in five locales, and the source reports how many
      entries it kept as summaries.

## How to verify

`cd apps/api && uv run pytest tests/test_news_automation.py -q`

## Notes

- The summary is not evidence: a person writes the story by hand or rejects it; the owner
  sees that it exists, which is the point.
- Claimed with `--force` on 2026-09-30: `2026-09-27-news-evidence-excerpts-stop-at-8` (codex-p1-news,
  status review) also lists `scanner.py`, but its PR #966 was closed unmerged on 2026-09-29, and
  this change only touches the article-fetch failure branch of `scan_source`.
