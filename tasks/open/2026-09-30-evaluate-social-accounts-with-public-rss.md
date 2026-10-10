---
id: 2026-09-30-evaluate-social-accounts-with-public-rss
title: Evaluate social accounts with public RSS as lead-only news sources
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-30T11:25:23Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/sources.json
---

# Evaluate social accounts with public RSS as lead-only news sources

## Why

The owner asked on 2026-09-30 whether X and other social media should be news sources.
Decision for now: not X (paid API, terms of service, x.com refuses crawlers, and a post is
not evidence under BRIEF.md). Companies do announce on social media first, so accounts with
a public, free RSS feed could be useful as `lead_only` sources: they can only ever produce a
lead, which the second-evidence matching (task `2026-09-24-attach-a-second-evidence-source-to`)
can pair with a first-party page.

## Definition of done

- [ ] For each publisher already in `sources.json`, record whether an official YouTube
      channel, Bluesky or Mastodon account with a public RSS feed exists (checked, not assumed).
- [ ] Measure first: a week after the 2026-09-30 source changes are deployed, count how many
      stories were still missed. Add `lead_only` social feeds only if that number says so.

## Notes

- No X, no scraping, no paid API without the owner's decision.
- 2026-10-10: the owner asked again, this time for the official X accounts to follow. The
  list, each checked against a first-party page, is in `docs/official-ai-accounts.md`. The X
  API is now pay-per-use only (https://docs.x.com/x-api/getting-started/pricing, read
  2026-10-10): $0.005 per post read, $0.010 per user read, at most 3 million post reads per
  billing cycle, no free tier. Following all 40 listed accounts was estimated at 30 to 42
  US dollars a month, assuming five to seven posts per account a day (assumed, not
  measured). The owner saw the price and decided not to use the API; a post would still be
  a lead and not evidence. The decision above stands.
