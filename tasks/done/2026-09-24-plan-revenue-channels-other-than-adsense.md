---
id: 2026-09-24-plan-revenue-channels-other-than-adsense
title: Plan revenue channels other than AdSense
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-09-24T00:27:09Z
created_at: 2026-09-24T00:26:50Z
completed_at: 2026-09-24T00:44:23Z
branch: claude/adsense-alternatives-plan-ce49cf
depends_on: []
scope:
  - docs/monetization-alternatives.md
  - docs/adsense-feasibility.md
---

# Plan revenue channels other than AdSense

## Why

AdSense rejected mokaair.com on 2026-09-23 as 缺乏價值的內容 (low value content). The
code has been ready since PR #449／#461 and stays off; what failed is the review. The owner
asked (2026-09-24) for a plan covering everything except AdSense: other ad networks, more
affiliate programmes, direct sponsorship, and first-party products or reader support.

Constraints the plan has to live with:

- Article pages see fewer than 3,000 views a month (owner's estimate). Google has only
  indexed the site since about 2026-09-14, and the repo holds no measured traffic numbers.
- The site's privacy rules: DNT/GPC means no third-party script at all, Consent Mode is
  always denied, the strict script CSP is enforced and relaxed only for article routes
  inside `app/(ads-public)`.
- The owner already decided on 2026-09-23 (`tasks/done/2026-09-23-reposition-the-site-as-a-travel.md`)
  to keep every lifestyle topic indexed and present the site as a travel-and-life guide.
  This plan does not reopen that.

This is an evaluation, not an implementation, in the same shape as `docs/adsense-feasibility.md`
(PR #448): one document, plus a ticket for every follow-up.

## Definition of done

- [x] `docs/monetization-alternatives.md` ranks the channels for this site today, with the
      eligibility, script weight, privacy cost and rough revenue of each, and every external
      figure carries a source and the date it was read.
- [x] The decisions only the owner can make are listed with a recommendation each.
- [x] Every follow-up has its own ticket in `tasks/open/`.
- [x] `docs/adsense-feasibility.md` says the application was rejected and points to the new document.

## Steps

- [x] Inventory the monetization code, the content mix and the programmes (three read-only agents, 2026-09-24).
- [x] Verify the hosting affiliate programmes that match the hosting guides in the repo.
- [x] Write `docs/monetization-alternatives.md`.
- [x] Add the rejection note to `docs/adsense-feasibility.md`.
- [x] File the follow-up tickets.
- [x] `npm run check:tasks`, PR.

## How to verify

```bash
npm run check:tasks
npm run tasks -- list | grep 2026-09-24
```

Read section 1 of `docs/monetization-alternatives.md`: the order should be something the
owner can start on without writing code.

## Notes

- Research used the `Mokaair-editorial-research` User-Agent and no personal data
  (memory: a subagent once put the owner's email into a User-Agent).
- The first draft said GetYourGuide and Viator only needed joining in Travelpayouts. On
  2026-09-07 they sat under "Unlock more" in project 570089 (`docs/travel-services.md`),
  while Tiqets, Airalo, Kiwitaxi and KKday were Available. The document now says so.
  Check that list before telling the owner a brand is one click away.
- The content-direction question (hide the non-travel articles or not) was already settled
  by the owner in `2026-09-23-reposition-the-site-as-a-travel`, so it is not re-asked here.
- Follow-ups filed: `2026-09-24-article-page-views-keep-the-article`,
  `-hosting-affiliate-links-in-the-hosting`, `-travelpayouts-drive-loads-on-share-token`,
  `-reader-support-link-at-the-end`, `-first-party-sponsor-placements-design`,
  `-take-payment-for-the-usage-packs`.
