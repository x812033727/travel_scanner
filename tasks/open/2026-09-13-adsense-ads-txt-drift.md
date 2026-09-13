---
id: 2026-09-13-adsense-ads-txt-drift
title: Serve ads.txt from the configured publisher id instead of a build-time file
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-13T09:44:42Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/public/ads.txt
  - apps/web/app/ads.txt
  - apps/web/e2e/guides-adsense.spec.ts
  - docs/travel-guides.md
---

# Serve ads.txt from the configured publisher id instead of a build-time file

## Why

`apps/web/public/ads.txt` hard-codes one publisher id at build time, while
`adsense_publisher_id` is changed from the back office without a redeploy — the whole point
of that card. Nothing checks that the two agree, so moving to a different AdSense account
gives a green admin card serving inventory Google treats as **unauthorised**, and the only
signal is a warning inside AdSense that nobody on this side is watching for.

Found by the pre-merge review of #449 and rated low: the owner has one account today, and
AdSense itself reports the mismatch. The stop-gap that shipped is a line in the
`adsense_publisher_id` help text (five locales) telling whoever changes it to change
`ads.txt` too. That is a note, not a guarantee.

## Definition of done

- [ ] `/ads.txt` is served from the configured publisher id rather than a checked-in file,
      so the two cannot disagree.
- [ ] It still answers when the API is unreachable — Google crawls this to verify the site,
      and an outage must not un-verify it. A hard-coded fallback is fine; silence is not.
- [ ] `proxy.ts:28`'s matcher skips paths containing a dot, so a route handler at
      `app/ads.txt/route.ts` is not locale-redirected. Confirm that still holds.
- [ ] Delete `apps/web/public/ads.txt` — a static file of the same name wins over the route.
- [ ] `e2e/guides-adsense.spec.ts`'s ads.txt case asserts the configured id, not a literal.
- [ ] Drop the stop-gap sentence from `admin.providerFields.adsense_publisher_id.help`
      in all five locales once it is no longer true.

## Steps

- [ ] `app/ads.txt/route.ts` reading `fetchAdsenseConfig()`, with the fallback constant.
- [ ] Remove the static file; update the e2e case and `docs/travel-guides.md`.

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
cd apps/web && npm run build && PLAYWRIGHT_SERVE_BUILD=true npx playwright test e2e/guides-adsense.spec.ts
```

Local: `curl -s localhost:3000/ads.txt` matches the id in the back office; change the id and
confirm the file changes without a rebuild; stop the API and confirm it still answers.

## Notes

- Format is one line: `google.com, pub-<16 digits>, DIRECT, f08c47fec0942fa0`. The stored id
  is `ca-pub-<16 digits>`, so the `ca-` prefix is dropped when rendering it.
- Not urgent. Only worth doing before the owner ever moves AdSense accounts.
