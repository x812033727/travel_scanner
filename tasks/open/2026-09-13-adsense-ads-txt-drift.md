---
id: 2026-09-13-adsense-ads-txt-drift
title: Serve ads.txt from the configured publisher id instead of a build-time file
status: review
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-19T09:27:35Z
created_at: 2026-09-13T09:44:42Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/web/public/ads.txt
  - apps/web/app/ads.txt
  - apps/web/e2e/guides-adsense.spec.ts
  - docs/travel-guides.md
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
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

- [x] `/ads.txt` is served from the configured publisher id rather than a checked-in file,
      so the two cannot disagree.
- [x] It still answers when the API is unreachable — Google crawls this to verify the site,
      and an outage must not un-verify it. A hard-coded fallback is fine; silence is not.
- [x] `proxy.ts:28`'s matcher skips paths containing a dot, so a route handler at
      `app/ads.txt/route.ts` is not locale-redirected. Confirm that still holds.
- [x] Delete `apps/web/public/ads.txt` — a static file of the same name wins over the route.
- [x] `e2e/guides-adsense.spec.ts`'s ads.txt case asserts the configured id, not a literal.
- [x] Drop the stop-gap sentence from `admin.providerFields.adsense_publisher_id.help`
      in all five locales once it is no longer true.

## Steps

- [x] `app/ads.txt/route.ts` reading `fetchAdsenseConfig()`, with the fallback constant.
- [x] Remove the static file; update the e2e case and `docs/travel-guides.md`.

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

### 2026-09-19 done in repo (claude-fable-5-1)

- `apps/web/app/ads.txt/route.ts`, plus `ads-txt.ts` beside it for the fallback constant and
  Google's line (a `route.ts` may export nothing but handlers and segment config, and the e2e
  imports the constant), and `route.test.ts`. `force-dynamic` like `llms.txt` and
  `sitemap.xml`: read when a crawler asks, never baked at build time where there is no API.
- Fallback: the handler reads `fetchAdsenseConfig()` — 1 s timeout on the API call, 60 s
  process-local cache, last good answer kept through up to 10 min of failed refreshes, never
  throws — and serves `google.com, pub-<16 digits>, DIRECT, f08c47fec0942fa0` from the
  configured id with the `ca-` prefix dropped. Whenever that answer carries no id (API
  unreachable for longer than the cache tolerates, advertising switched off, id empty, or an
  id not in Google's shape) or the read itself throws, it serves
  `ADS_TXT_FALLBACK_PUBLISHER_ID` = `ca-pub-4140966684432854`, the id the deleted
  `public/ads.txt` named. Always 200 `text/plain; charset=utf-8`, one line, trailing newline.
  Residual window: an outage longer than 10 min falls back to the constant, so if the owner
  ever moves accounts, bump the constant in `ads-txt.ts` in the same change as the
  back-office id — then the two can only disagree during such an outage, not permanently.
- Cache: `Cache-Control: public, max-age=3600`. Nothing between Google and the server caches
  today; the header lets anything that ever does serve its copy for an hour, and Google
  re-reads ads.txt about daily, so a changed id still reaches the next crawl with no redeploy.
  The article pages read the same configuration through the 60 s cache, so the two stay
  within an hour of each other at worst.
- Proxy: the matcher now lives at the bottom of `proxy.ts`, `/((?!api|_next|_vercel|.*\..*).*)`,
  and skips any path containing a dot. Confirmed by compiling it with Next's own
  `next/dist/compiled/path-to-regexp` (the options `getMiddlewareMatchers` uses): `/ads.txt`,
  `/llms.txt`, `/robots.txt` and `/sitemap.xml` do not match; `/`, `/guides` and
  `/zh-TW/guides/howto/tokyo-esim` do. So `/ads.txt` never reaches next-intl and is not
  redirected to a locale; `Cache Components` is off in `next.config.ts`, so the `dynamic`
  export is still honoured.
- e2e: the fixture's `PUBLISHER` is now `ca-pub-1234567890123456`, deliberately not the
  fallback, and the ads.txt case asserts the line built from it, `text/plain`, and a 200 with
  `maxRedirects: 0`, guarded by `expect(PUBLISHER).not.toBe(ADS_TXT_FALLBACK_PUBLISHER_ID)` —
  it can only pass when the file is built from what the API double answered. Not run here
  (needs `next build` + Playwright); run the second line of "How to verify" before merging.
- Copy: the stop-gap sentence is gone from `admin.providerFields.adsense_publisher_id.help` in
  all five locales, one line each; nothing else in those files touched. Scope widened to those
  five files for it.
- `docs/travel-guides.md` "Advertising" → **ads.txt** bullet rewritten for the route.
- Checks: `npm run lint:web`, `npm run typecheck:web` (covers `e2e/**` too), `npm run check:i18n`
  and `npm run check:tasks` clean; `npx vitest run app/ads.txt lib/adsense` 70/70, and the
  full `npm run test:web` 289 files / 3164 tests green.
