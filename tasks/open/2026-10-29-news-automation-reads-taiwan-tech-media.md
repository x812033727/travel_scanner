---
id: 2026-10-29-news-automation-reads-taiwan-tech-media
title: News automation reads Taiwan tech media as lead-only sources
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-10-29T02:14:14Z
created_at: 2026-10-29T02:13:30Z
completed_at:
branch: claude/dazzling-wright-pqolfx
depends_on: []
scope:
  - apps/api/app/news_automation/sources.json
  - apps/api/tests/test_news_automation.py
  - apps/api/app/news_automation/scanner.py
  - docs/news-automation.md
---

# News automation reads Taiwan tech media as lead-only sources

## Why

The owner asked why 電腦王阿達 (kocpc.com.tw) carries so many AI stories the news automation
never sees (2026-10-29). It is not press releases: of its 150 AI posts before that day, the
outbound links went most often to x.com (69 posts counting t.co), github.com (21),
reddit.com (10), openai.com and blog.google (9 each). Its writers find new AI tools and
features on X, GitHub and Reddit, then write them up from the official page. We had no
source that reads Taiwan tech media at all, so we never learned of these stories even when
an official page we do read backs them.

## Definition of done

- [x] 電腦王阿達 and iThome are `lead_only` sources: a post that links to a page on an
      evidence source files a candidate drafted from that page, the post kept as uncited
      context.
- [x] A lead-only post that links to no evidence page is closed at once as `rejected`
      (`news_lead_without_evidence`), not left in `needs_evidence` where nothing would ever
      attach to it.
- [ ] Loaded on the host with `sources_cli --source-url` for each of the two URLs after the
      deploy, and a week later the share of their posts that drafted is written below.

## How to verify

```bash
cd apps/api && uv run pytest -q tests/test_news_automation.py -k lead_only_page
```

## Notes

- Probed 2026-10-29 from a cloud container through the scanner's own fetch and parse code
  (IP pinning switched off for the container's proxy): 2 of 11 Taiwan-media posts linked to
  an evidence source (kocpc -> deepmind.google, iThome -> blog.google). Expect a modest
  yield; the rest link to X, GitHub, Reddit or other media, which task
  `2026-10-29-news-automation-drafts-notable-new-ai` addresses for GitHub and tool sites.
- Left out: INSIDE and TechNews (their posts link to other media, cnyes, Nikkei, not
  official pages; TechNews also spreads posts over finance./info. subdomains),
  TechOrange (feed redirects off-host), 數位時代 (no /rss).
- kocpc: category feeds are disallowed by robots.txt (`/*/feed`); the site feed covers
  games and deals, so titles are filtered by keyword (28 of the newest 100 passed). Post
  pages wrap related-post cards in `<article>`, hence `article_classes: content-inner`.
- iThome: entries are undated (the first scan is all baseline); the default read takes in
  rotating related-news lists, hence `content-summary` and `field-name-body`.
- X is kocpc's main source; reading it needs the paid X API. The owner chose to leave it
  for now (2026-10-29).
