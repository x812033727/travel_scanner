---
id: 2026-09-12-affiliate-cta-guides-and-city-pages
title: Affiliate CTAs on guide articles and destination city pages
status: in-progress
priority: P2
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-12T05:36:31Z
created_at: 2026-09-12T05:36:17Z
completed_at:
branch: claude/affiliate-controls-and-guide-cta
depends_on:
  - 2026-09-12-affiliate-placement-tracking
scope:
  - apps/web/lib/guide-affiliate.ts
  - apps/web/lib/guide-affiliate.test.ts
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/components/destination-guide.tsx
  - apps/web/components/destination-guide.test.tsx
  - apps/web/components/travel-services/admin.tsx
  - apps/web/components/travel-services/admin.test.tsx
  - docs/travel-guides.md
---

# Affiliate CTAs on guide articles and destination city pages

## Why

`/guides/{kind}/{slug}` and `/destinations/{id}` are the highest-value indexable pages and
carried no partner entrance and no disclosure. Both already know their destination, so the
existing anonymous `DestinationAffiliateOptions` panel can end them without a schema change.

## Definition of done

- [x] A published, unexpired article with a destination and a monetisable topic ends with the
      partner panel labelled `placement="guide"`, showing only the modules its topics map to.
- [x] Cross-destination articles, expired notices and topics with no honest module show nothing.
- [x] The city page mounts the panel for all modules as `placement="city"`.
- [x] Operators can open or close the two surfaces from Release controls without a deploy.
- [x] No new i18n keys: the panel and the checkboxes reuse existing copy.

## Steps

- [x] `lib/guide-affiliate.ts`: topic to module allowlist, Kyoto folds into `osaka-kyoto`.
- [x] Mount in `components/guides/article.tsx` and `components/destination-guide.tsx`.
- [x] Release-controls checkboxes in `travel-services/admin.tsx`.

## How to verify

```
cd apps/web && npx vitest run lib/guide-affiliate.test.ts components/guides/article.test.tsx components/destination-guide.test.tsx components/travel-services/admin.test.tsx
```

Then on production: enable `guide` in Release controls, approve one destination offer for a
city, publish an article for that city with a matching topic, and check the panel, the
disclosure and a 303 click that lands as `placement='guide'` in `affiliate_clicks`.

## Notes

`hotspot-explorer.tsx` and the in-article `offer` block are deliberately out of scope: the
first is claimed by the site-experience task, the second needs new admin message keys
(`2026-09-12-guide-offer-content-block`).
