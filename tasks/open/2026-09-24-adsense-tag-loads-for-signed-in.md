---
id: 2026-09-24-adsense-tag-loads-for-signed-in
title: AdSense tag loads for signed-in administrators
status: blocked
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-24T05:14:03Z
completed_at:
branch:
depends_on:
  - 2026-09-24-enforce-connect-src-on-private-routes
scope:
  - apps/web/components/ads/adsense-loader.tsx
  - apps/web/components/ads/adsense-loader.test.tsx
  - apps/web/app/[locale]/layout.tsx
---

# AdSense tag loads for signed-in administrators

## Why

`2026-09-24-enforce-connect-src-on-private-routes` (retitled "Administrators never load
third-party scripts") keeps Travelpayouts Drive and GA4's `gtag.js` out of an administrator's
browser. The reason: a vendor script can call the admin API same-origin with the owner's
cookies from any page. Google's AdSense tag has the same reach and was left out of that change.

On an article page with ads switched on, `app/[locale]/layout.tsx` renders `<AdsenseLoader>` for
every reader. That document is deliberately anonymous: it never calls `/auth/me`, so it
cannot tell an administrator apart. The owner reading their own article with ads on would run
the ad tag with an admin session.

**Blocked**: AdSense was rejected on 2026-09-23 and ads are off in the admin settings, so no
document loads the tag today. Do this before ads are switched back on.

## Definition of done

- [ ] With a session cookie present, an ads article page does not load the AdSense tag. The
      layout knows the cookie (`hasSession`) but not the role, so every signed-in reader is
      treated alike, the same rule `ThirdPartyAudience` uses for `unknownRole`.
- [ ] Signed-out readers see ads exactly as before.

## Steps

- [ ] Decide with the owner first. Skipping ads for every signed-in reader costs a little
      revenue; the alternative is asking `/auth/me` on ad pages, which the anonymous-document
      design exists to avoid.
- [ ] Gate `<AdsenseLoader>` and the article slots on it; tests.

## How to verify

With ads on in a test environment: signed out, the tag loads; with a `travel_access`
cookie, it does not.

## Notes

- Filed 2026-09-24 while doing the administrator gate for Drive and GA4.
