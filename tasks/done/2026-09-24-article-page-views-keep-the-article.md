---
id: 2026-09-24-article-page-views-keep-the-article
title: Article page views keep the article slug
status: done
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-24T01:05:06Z
created_at: 2026-09-24T00:29:57Z
completed_at: 2026-09-24T01:13:19Z
branch: claude/article-pageviews-keep-slug
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

- [x] A view of `/zh-TW/life/<slug>` or `/{locale}/guides/{intel,howto}/<slug>` is stored
      with the full slug, up to the 128-character `analytics_events.normalized_path`
      column: a `/guides/intel/` slug of up to 114 characters (the schema allows 120; the
      longest today is 53). Widening the column for six characters no slug uses is not worth
      a migration.
- [x] Every other path still collapses long segments to `:id`: `/share/<token>`, trip ids,
      and anything that is not one of those two article shapes.
- [x] Tests on both ends prove both halves.

## Steps

- [x] Match the article shape after the locale is stripped, the same shapes
      `adsenseArticleRoute` in `apps/web/lib/adsense.ts` accepts; keep the slug segment only
      when it matches the article slug rule (lowercase letters, digits, hyphens).
- [x] `normalize_path` truncates each part to 48 characters and the whole path to 128.
      Keep the whole slug for article paths, or two slugs with the same 48-character prefix
      will merge.
- [x] Mirror the rule in `sanitizedPath` so the browser does not destroy the slug before
      the server sees it.
- [x] Tests: article paths keep the slug; `/zh-TW/share/<22-char token>` and a UUID trip
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
- 2026-09-24, found while fixing it: the collapse also **dropped views**, not only merged
  them. `AnalyticsProvider` skips a `page_view` whose sanitized path equals the previous
  one (`lastPage`), so reading one long-slug article after another in the same tab sent a
  single view: both were `/life/:id`. First-party page-view totals before this deploy are
  undercounts for article-to-article browsing, not only unsplittable. The web test
  "counts a second long-slug article as its own page view" failed on the old component.
- Both halves were checked against the pre-fix code: the new API test and three of the new
  web tests fail there; the token-folding tests pass on both, as regression guards.
- Local run on Windows: `mypy tests` reports `socketserver.UnixStreamServer` in
  `tests/support/e2e_deploy_agent.py`, a Windows-only error unrelated to this change.
