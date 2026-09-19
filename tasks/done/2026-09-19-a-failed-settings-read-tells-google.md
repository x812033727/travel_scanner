---
id: 2026-09-19-a-failed-settings-read-tells-google
title: A failed settings read tells Google noindex
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-19T14:41:50Z
created_at: 2026-09-19T14:41:40Z
completed_at: 2026-09-19T16:00:05Z
branch: claude/google-indexing-issues-efbfb9
depends_on: []
scope:
  - apps/web/lib/site-visibility.server.ts
  - apps/web/lib/site-visibility.server.test.ts
  - apps/web/lib/site-features.ts
  - apps/web/lib/site-features.test.ts
  - apps/web/components/public-feature-gate.tsx
---

# A failed settings read tells Google noindex

## Why

`lib/site-visibility.server.ts` returned `closedSiteVisibility` on **any** non-200, malformed
body or 3-second timeout, and `featureEnabled` read that as "the owner closed this feature".
The consequence was not a closed page but a lie told to a crawler: `/hotspots`, `/pricing`,
`/flights/status` and `/labs/airlines` emitted `<meta name="robots" content="noindex">`, and
the same request dropped those routes from the sitemap. One slow moment while Googlebot is
reading is enough for it to record the URL as noindexed, and it keeps believing that long
after the blip is over.

Found while auditing indexing, not from a report -- 45 sampled sitemap URLs all came back
indexable, so this was latent rather than firing. It became worth fixing anyway once
`2026-09-19-orphan-pages-hotspots-foods-and-explore` made the footer the only inbound link
`/hotspots` has: a settings blip that noindexes it now costs more than it used to.

## Definition of done

- [x] a failed or timed-out settings read no longer produces `noindex` on a live page
- [x] closing a feature in the admin console still takes effect immediately
- [x] a feature genuinely closed stays `noindex`

## Steps

- [x] third status `stale` on `SiteVisibilityState`, carrying the last answer the service gave
- [x] module-scope last-good snapshot in `loadSiteVisibility`, bounded to 10 minutes
- [x] `featureEnabled` closes only on `unavailable`; `featureVisible` uses real flags when it
      has them
- [x] the home page reads through `featureEnabled` instead of its own inline status check
- [x] `site-visibility.server.test.ts` rewritten, new `site-features.test.ts` (11 passed)

## How to verify

```bash
npx vitest run lib/site-visibility.server.test.ts lib/site-features.test.ts   # 11 passed
```

The two cases that carry the intent: "keeps the last answer the service gave when a later
read fails" and "lets a successful read replace a remembered one immediately" -- the second is
what keeps the admin toggle honest.

Deployed in #566 (`ecc6cbc0`) on 2026-09-19.

## Notes

`PublicFeatureGate` needed no change and that is worth stating: on `stale` with the feature
closed it still falls to the closed branch and shows `CircleOff`, while `unavailable` keeps
the `TriangleAlert` "could not read the settings" icon. The distinction the component already
drew turned out to be exactly the one this change needed.

`app/sitemaps/sitemap.ts` also needed no change, which is why this fitted in a scope that
excluded it: it reads `featureEnabled(visibility, route.feature)`, so widening that helper
fixed the sitemap side for free. That file is held by
`2026-09-14-sitemap-lists-pet-friendly-places`.

The bounded window is the part to revisit if it ever bites: a closed feature stays open for up
to 10 minutes **only while the settings service is unreachable**. Any successful read wins
immediately.
