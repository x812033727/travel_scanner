---
id: 2026-09-24-article-page-views-keep-the-article
title: Article page views keep the article slug
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-24T00:29:57Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/analytics/service.py
  - apps/api/tests/test_analytics.py
  - apps/api/tests/test_analytics_integration.py
  - apps/web/components/analytics-provider.tsx
  - apps/web/components/analytics-provider.test.tsx
---

# Article page views keep the article slug

## Why

The first-party analytics cannot say how many people read a given article, so no revenue
channel can be judged per article (`docs/monetization-alternatives.md`, section 6). Both
ends replace any path segment of 20 or more `[A-Za-z0-9_-]` characters with `:id`, to keep
share tokens and UUIDs out of the data:

- `apps/api/app/analytics/service.py:80` (`_UUID_OR_TOKEN`), applied by `normalize_path`.
- `apps/web/components/analytics-provider.tsx:45` (`sanitizedPath`).

Article slugs are public, human-readable and often that long: about 998 of the 1,117 packs
in `apps/api/app/guides/content` have one (2026-09-24 count). Their views all land on
`/life/:id` or `/guides/howto/:id`. Affiliate clicks, by contrast, already carry
`article_slug` (PR #565), so clicks per article exist but views per article do not, and
click-through or earnings per view cannot be computed.

## Definition of done

- [ ] A view of `/zh-TW/life/<slug>` or `/{locale}/guides/{intel,howto}/<slug>` is stored
      with the full slug, for any published slug length (schema max is 120; the longest
      today is 53).
- [ ] Every other path still collapses long segments to `:id`: `/share/<token>`, trip ids,
      and anything that is not one of those two article shapes.
- [ ] Tests on both ends prove both halves.

## Steps

- [ ] Match the article shape after the locale is stripped, the same shapes
      `adsenseArticleRoute` in `apps/web/lib/adsense.ts` accepts; keep the slug segment only
      when it matches the article slug rule (lowercase letters, digits, hyphens).
- [ ] `normalize_path` truncates each part to 48 characters and the whole path to 128.
      Keep the whole slug for article paths, or two slugs with the same 48-character prefix
      will merge.
- [ ] Mirror the rule in `sanitizedPath` so the browser does not destroy the slug before
      the server sees it.
- [ ] Tests: article paths keep the slug; `/zh-TW/share/<22-char token>` and a UUID trip
      path still become `:id`.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_analytics.py tests/test_analytics_integration.py -q
cd apps/web && npx vitest run components/analytics-provider.test.tsx
```

After a deploy, open one long-slug article, then check `/admin/analytics` shows that path
rather than `/life/:id`.

## Notes

- Views recorded before the fix cannot be split back out; comparisons start at the deploy date.
- Rollups keep route and locale as separate dimensions (`service.py` rollup code), so this
  gives views per article, not per article per locale. That is enough to rank articles;
  split it only if a channel needs per-locale numbers.
- Found while planning revenue channels (`2026-09-24-plan-revenue-channels-other-than-adsense`).
