---
id: 2026-09-30-microsoft-official-blog-and-the-block
title: Microsoft official blog and The Block refuse the news scanner (Cloudflare 403): find readable pages or demote to lead_only
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-30T11:04:55Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/sources.json
---

# Microsoft official blog and The Block refuse the news scanner (Cloudflare 403): find readable pages or demote to lead_only

## Why

The listings of `Microsoft official blog` (blogs.microsoft.com) and `The Block` (theblock.co) load,
but every article page answers 403 from Cloudflare, with our UA and with curl's alike.
`news.microsoft.com/source/feed/` loads too, and its newest entry points at blogs.windows.com,
which is also 403. Until the scanner fallback of 2026-09-30, every entry of these two sources
was skipped every hour; with it, each recent entry becomes a `news_page_refused` lead. Found 2026-09-30 by fetching every source in `sources.json` the way the scanner does (listing, then the two newest articles, UA `Mokaair-editorial/1.0`), from a cloud container rather than the host.

## Definition of done

- [ ] On the host, confirm in `/admin/news` that both sources sit at `partial` with
      `HTTPStatusError` skips (the host's IP may be treated differently).
- [ ] Microsoft: find a first-party page the scanner can read (a news.microsoft.com
      story page, the Microsoft Source regional sites, an official API) or record that none
      exists.
- [ ] The Block: CoinDesk and Decrypt cover the same crypto news and are readable; set it to
      `lead_only` or disable it, so it stops filling the review queue with leads.
