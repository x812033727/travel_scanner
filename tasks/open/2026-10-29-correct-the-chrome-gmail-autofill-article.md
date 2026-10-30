---
id: 2026-10-29-correct-the-chrome-gmail-autofill-article
title: Correct the Chrome Gmail autofill article: Google removed the Google Photos plan
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-29T04:49:17Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-29-correct-the-chrome-gmail-autofill-article.md
---

# Correct the Chrome Gmail autofill article: Google removed the Google Photos plan

## Why

The published article `ai-news-chrome-autofill-gmail-20261028`
(https://mokaair.com/zh-TW/life/ai-news-chrome-autofill-gmail-20261028) says Google plans to
extend enhanced autofill to information in Google Photos. Google's own post
(blog.google, "enhanced autofill" with Gmail) no longer says so: on 2026-10-29 neither its text
nor its raw HTML mentions Photos, and the page shows it was modified at 2026-10-28 20:21 UTC,
after the site article was published at 17:19 UTC. Found by the fact check of the daily brief
episode `daily-ai-20261028` (`docs/videos/daily-ai-20261028/verify-1.md`, claim 4nia), which
dropped the sentence from the video.

The article was written by the news automation, so it lives in the database, not in
`apps/api/app/guides/content/`; the correction goes through /admin/news (re-check the evidence
and re-verify) or the guide editor.

## Definition of done

- [ ] The Photos sentence is removed from the zh-TW article and every published locale,
      with the evidence re-checked against Google's current post.

## Notes

- Scope is this file only: the fix is a database edit on the host, not a repository change.
