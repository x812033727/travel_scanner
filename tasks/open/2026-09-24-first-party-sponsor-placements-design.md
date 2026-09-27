---
id: 2026-09-24-first-party-sponsor-placements-design
title: First-party sponsor placements design
status: blocked
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-09-24T00:30:21Z
completed_at:
branch:
depends_on:
  - 2026-09-24-article-page-views-keep-the-article
scope:
  - docs/sponsor-placements.md
---

# First-party sponsor placements design

## Why

Selling a placement directly (a tourism board, a hotel, an eSIM brand paying a flat fee
for a card on a city page or in articles) is the only kind of advertising that fits every
privacy rule the site has: the site renders the card itself from its own database, so there
is no third-party script, no consent banner and no CSP change
(`docs/monetization-alternatives.md`, section 4.3).

Nothing existing can carry it. The brand and destination-offer tables are for affiliate
links only: `ck_service_brand_channel` allows `travelpayouts` and `klook_direct`
(`apps/api/app/models.py:386`), readiness needs affiliate credentials, and the disclosure is
commission wording. A sponsor card needs fields none of them have: advertiser and creative,
a 廣告 label (not 合作連結), start and end dates, targeting by locale and page, and an
impression count, since sponsors pay for being seen and the site logs no impressions today.

**Blocked on the owner (decision D5)**, and on demand: at under 3,000 article views a month
no sponsor will pay enough to cover the build. Reopen when either a real advertiser asks,
or article views pass about 30,000 a month (measurable once
`2026-09-24-article-page-views-keep-the-article` lands).

## Definition of done

- [ ] `docs/sponsor-placements.md` specifies the data model, admin flow, rendering rules,
      disclosure per locale, impression and click counting, and what a sponsor may not buy.
- [ ] The owner has approved it; the build is filed as its own tickets.

## Steps

- [ ] Write down the rules first: labelled 廣告／広告／광고／Ad; never above the article's
      first section; never inside the planner, share or account pages; no sponsor in
      a slot that ranks or reviews its own category; no sponsor that competes with an
      affiliate partner on the same card.
- [ ] Data model: a new table, not a new channel on `TravelServiceBrand`.
- [ ] Impression counting that stores no personal data (count per slot per day, first party).
- [ ] A one-page rate card the owner can send: audience, locales, monthly views, placements, price.

## How to verify

The owner reads `docs/sponsor-placements.md` and approves or amends it.

## Notes

- Reuse, do not copy: the clickout pattern (same-origin POST, 303, `no-referrer`) and
  `affiliate_clicks` for click counts; the `(ads-public)` placement rules for spacing from
  partner buttons (`apps/web/lib/adsense.ts`, `adsensePlacements`).
