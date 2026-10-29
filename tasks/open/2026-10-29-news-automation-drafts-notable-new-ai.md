---
id: 2026-10-29-news-automation-drafts-notable-new-ai
title: News automation drafts notable new AI tools from their own repo or site
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-29T02:13:32Z
completed_at:
branch:
depends_on:
  - 2026-10-29-news-automation-reads-taiwan-tech-media
scope:
  - apps/api/app/news_automation/ai.py
  - apps/api/app/news_automation/judge.py
  - apps/api/app/news_automation/policy.py
  - apps/api/tests/test_news_automation.py
---

# News automation drafts notable new AI tools from their own repo or site

## Why

電腦王阿達's AI category is mostly new tools and features (open-source apps, a new ChatGPT
setting), sourced from a GitHub README or the tool's own site. Our writer
(`WRITER_INSTRUCTIONS` in `apps/api/app/news_automation/ai.py`) reports only "generally
important" events and excludes marketing and minor promotions, and github.com is not a
source, so none of these can be drafted even when a lead-only source finds them. The owner
chose this as the second step after the lead sources (2026-10-29).

## Definition of done

- [ ] A story about a new tool or feature can be drafted when its only evidence is the
      project's own page (GitHub repository or official site), within a bar the owner
      approves (for example a star threshold, or a second outlet reporting it).
- [ ] The article may carry a short "how to start" section built only from steps on that
      page; no command or step the evidence does not show.
- [ ] The review judge (`judge.py`) applies the same bar, and tests cover a tool story
      that passes and one that does not.

## Notes

- Decide with the owner before coding: what makes a tool notable, and whether github.com
  repository pages become an evidence host (they would need a source row; the scanner only
  follows links to hosts that are enabled evidence sources).
