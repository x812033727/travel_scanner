---
id: 2026-09-30-microsoft-official-blog-and-the-block
title: Microsoft official blog and The Block refuse the news scanner (Cloudflare 403): find readable pages or demote to lead_only
status: review
priority: P2
area: api
owner: claude-opus-5-5-news-4-9
claimed_at: 2026-09-30T12:20:14Z
created_at: 2026-09-30T11:04:55Z
completed_at:
branch: claude/gifted-rubin-umw5s4
depends_on: []
scope:
  - apps/api/app/news_automation/sources.json
  - apps/api/app/news_automation/scanner.py
  - docs/news-automation.md
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
- [x] Microsoft: find a first-party page the scanner can read (a news.microsoft.com
      story page, the Microsoft Source regional sites, an official API) or record that none
      exists.
- [x] The Block: CoinDesk and Decrypt cover the same crypto news and are readable; set it to
      `lead_only` or disable it, so it stops filling the review queue with leads.

## Notes

- 2026-09-30: **The Block disabled** in `sources.json`. With the refused-page fallback it would
  have turned every article into a lead; the fallback is now first-party only
  (`source.is_first_party`), since a refused press page is not worth a hand-written story.
- **Microsoft stays enabled.** The survey found no readable first-party alternative
  (news.microsoft.com, its Source feed's links to blogs.windows.com, and the Windows blog all
  answer Cloudflare 403). Its recent refused entries become `news_page_refused` leads, and the
  Microsoft Research blog (readable) remains a source.
- Left: confirm both 403s from the host (first box).
