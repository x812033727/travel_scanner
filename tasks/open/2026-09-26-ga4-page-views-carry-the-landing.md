---
id: 2026-09-26-ga4-page-views-carry-the-landing
title: GA4 page views carry the landing page's campaign tags
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-26T03:34:20Z
completed_at:
branch:
depends_on:
  - 2026-09-26-article-pages-keep-their-query-string
scope:
  - apps/web/components/analytics-provider.tsx
  - apps/web/components/analytics-provider.test.tsx
---

# GA4 page views carry the landing page's campaign tags

## Why

The YouTube pipeline links each video's article with
`utm_source=youtube&utm_medium=video&utm_campaign=<slug>` (`tools/video/core/metadata.mjs`
`articleUrl`), and newsletter or social links carry the same kind of tags. Once
`2026-09-26-article-pages-keep-their-query-string` lands, the query reaches the article page,
and first-party analytics records the three tags (`initialCampaign()` in
`components/analytics-provider.tsx`). GA4 still does not: `initializeGa4` sets
`page_location` to `origin + sanitizedPath(pathname)` and `sendGa4Event` sends the same, so
the query is gone before gtag sees it. GA4 reads campaign attribution from the `utm_*`
parameters of `page_location`, so those sessions show up as `youtube.com / referral` at best.

## Definition of done

- [ ] The first GA4 `page_view` of a document carries the landing URL's `utm_source`,
      `utm_medium` and `utm_campaign` in `page_location`, cleaned exactly the way
      `initialCampaign()` cleans them; later page views in the document carry none.
- [ ] No other query parameter reaches GA4: search terms, ids and tokens stay out.
- [ ] DNT/GPC still sends nothing.

## Steps

- [ ] Build the landing `page_location` from `sanitizedPath` plus the cleaned campaign, in
      `initializeGa4` and the first `sendGa4Event("page_view")`.
- [ ] Tests in `analytics-provider.test.tsx`: tags on the first page view only, an unknown
      parameter dropped, a tag value with disallowed characters cleaned.
- [ ] After deploy, open an article with the three tags and confirm in GA4 Realtime /
      DebugView that the session's source, medium and campaign are the tags.

## How to verify

```bash
cd apps/web && npx vitest run components/analytics-provider.test.tsx
```

## Notes

- Same code path as route B of `2026-09-13-google-ads-conversion-measurement` (keep
  `gclid`/`gbraid`/`wbraid` in the landing `page_location`). Write the allow-list so that
  ticket only has to add three keys.
- Consent Mode defaults every storage to `denied` (`initializeGa4`), so GA4 receives
  cookieless pings. Check what the property actually shows for those before relying on GA4
  acquisition reports; the first-party dashboard already has the tags.
