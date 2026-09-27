---
id: 2026-09-26-add-ten-official-and-press-news
title: Add ten official and press news sources the owner picked
status: done
priority: P2
area: api
owner: claude-opus-5-5-news-final-editor
claimed_at: 2026-09-26T08:00:00Z
created_at: 2026-09-26T08:00:00Z
completed_at: 2026-09-26T08:10:00Z
branch: claude/news-more-sources
depends_on: []
scope:
  - apps/api/app/news_automation/sources.json
---

# Add ten official and press news sources the owner picked

## Why

The hourly news reads 12 enabled feeds and gets 20 to 40 new items a day. Only stories with
a first-party page may publish on their own, and most items come from three press feeds.
On 2026-09-26 the owner asked for more official sources and picked these from a list that
was validated on the production host with `sources_cli --file` (dry run).

## Definition of done

- [x] Added and validated from the host:
  - Meta Newsroom
  - AWS Machine Learning Blog
  - Microsoft Research blog
  - Google Keyword blog
  - Google Cloud blog (articles on `cloud.google.com`, so that host is an allowed redirect)
  - GitHub blog
  - Cloudflare blog
  - SEC press releases
  - Chainalysis blog
  - Decrypt (press)
- [ ] After deploy: `sources_cli --apply --actor-email <admin>`.

## How to verify

The dry run on the host lists the ten as `create`, each `valid: true`.

## Notes

These candidates could not be added, as of 2026-09-26:

- **robots.txt forbids our fetcher:**
  - Ars Technica (both the site and `feeds.arstechnica.com`)
  - Federal Reserve press releases
  - Kraken blog
  - Intel Newsroom
- **Timed out from the host:** Samsung Global Newsroom
- **Refused with 403 or 404:**
  - Coinbase blog
  - Circle blog
  - OpenAI News and The Block, which were already listed but never enabled
