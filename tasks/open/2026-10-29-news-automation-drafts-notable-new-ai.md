---
id: 2026-10-29-news-automation-drafts-notable-new-ai
title: News automation drafts notable new AI tools from their own repo or site
status: review
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-10-29T03:15:03Z
created_at: 2026-10-29T02:13:32Z
completed_at:
branch: claude/dazzling-wright-pqolfx
depends_on:
  - 2026-10-29-news-automation-reads-taiwan-tech-media
scope:
  - apps/api/app/news_automation/ai.py
  - apps/api/app/news_automation/scanner.py
  - apps/api/app/news_automation/feeds.py
  - apps/api/app/news_automation/validation.py
  - apps/api/app/news_automation/sources.json
  - docs/news-automation.md
  - apps/api/app/news_automation/judge.py
  - apps/api/app/news_automation/policy.py
  - apps/api/tests/test_news_automation.py
  - apps/api/tests/test_news_judge.py
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

- [x] A story about a new tool can be drafted when its only evidence is its GitHub
      repository page, within the owner's bar: 500 or more stars, and another outlet
      reported it (a repository is only ever read from a link on another source's page).
- [x] The article may carry a short "how to start" section built only from steps on that
      page; no command or step the evidence does not show.
- [x] The review judge applies the same bar (`JUDGE_REVIEW_INSTRUCTIONS`), and tests
      cover a repository above the minimum, one below it, and one with no star counter.
- [ ] After the deploy, `sources_cli --source-url https://github.com/ollama/ollama` passes
      on the host (robots and the star counter read from there), and the first tool
      stories are checked by hand.

## Notes

- Owner decisions 2026-10-29: 500 stars plus another outlet's report; tool stories are not
  published automatically, they wait for a person or the review judge.
- How: a `follow_only` source (never claimed by `claim_due_sources`, never scanned) puts
  github.com among the followed hosts; `repository_min_stars` on it makes the scanner read
  any link into a repository as its root page and keep it as evidence only at or above the
  minimum (`feeds.github_star_count` reads the counter's exact `title`). The source is not
  first-party and not `auto_publish_alone`, so `auto_evidence_ok` stays false.
- Not verified from the cloud container: its proxy answers 403 to every github.com
  repository page except this project's, so the star-counter markup was taken from GitHub's
  public page format and must be confirmed on the host (validation fails closed with
  「找不到 GitHub 星數」 if it differs).
- The prompt text changed but `prompt_version` (an admin setting, default `news-v1`) was
  not bumped; bump it in /admin/news if drafts should record the new rules.
