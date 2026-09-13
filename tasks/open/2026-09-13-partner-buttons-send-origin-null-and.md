---
id: 2026-09-13-partner-buttons-send-origin-null-and
title: Partner buttons send Origin null and the BFF refuses every click
status: in-progress
priority: P0
area: web
owner: claude-opus-5
claimed_at: 2026-09-13T04:21:25Z
created_at: 2026-09-13T04:20:49Z
completed_at:
branch: claude/travel-guide-klook-link-broken-2587c7
depends_on: []
scope:
  - apps/web/components/destination-affiliate-options.tsx
  - apps/web/components/destination-affiliate-options.test.tsx
  - apps/web/components/travel-services/catalog.tsx
  - apps/web/components/travel-services/catalog.test.tsx
  - apps/web/e2e/travel-services.spec.ts
---

# Partner buttons send Origin null and the BFF refuses every click

## Why

Reported 2026-09-13: the Klook buttons inside 旅遊情報攻略 articles do not open. Every partner
button that `DestinationAffiliateOptions` renders — guide and life articles, city pages, the trip
planner's day blocks, the share page, the services page — was a
`<form method="post" target="_blank" rel="noopener noreferrer">`. `noreferrer` gives the
submission the `no-referrer` policy, and for a non-GET navigation the browser then sends
`Origin: null`. The BFF (`app/api/travel/[...path]/route.ts`, `isAllowedMutationOrigin`) lets a
POST through only with a same-origin `Origin`, so the new tab showed
`{"status":403,"code":"cross_site_request_blocked","detail":"不允許跨網站修改資料"}` and the API
never saw the click. The hotel-link and product-offer forms in `catalog.tsx` carried the same
attribute. `booking-panel.tsx` was changed to `noopener` in #379 for exactly this reason and
`docs/stay22-allez.md` states the rule; these three forms never got it.

Nothing caught it: the unit tests asserted `noopener noreferrer`, the travel-services e2e fixture
fulfils the clickout inside the browser before the BFF's guard runs, and the production-HTTP e2e in
`stay22-allez.spec.ts` posts with a hand-written `Origin` header.

## Definition of done

- [x] A click on a destination-offer, hotel-link or product-offer button reaches the API with the
      page's own `Origin` and opens the partner page.
- [x] The e2e fixture records the `Origin` of every clickout POST and each popup test asserts it,
      so a `noreferrer` form fails CI rather than production.

## Steps

- [x] Reproduce on production in real Chromium (Playwright): `Origin: null` → 403 JSON page.
- [x] `rel="noopener"` on the three forms; unit assertions updated.
- [x] `e2e/travel-services.spec.ts`: `mock()` returns `clickoutOrigins`, every popup test asserts
      it, and the discovery test now clicks a destination offer. Red before the fix (`["null"]`),
      green after.

## How to verify

```bash
cd apps/web && npx vitest run components/destination-affiliate-options.test.tsx components/travel-services/catalog.test.tsx
npm run build && PLAYWRIGHT_SERVE_BUILD=true npx playwright test e2e/travel-services.spec.ts
```

After deploying: open `https://mokaair.com/zh-TW/guides/howto/tokyo-5-day-itinerary` in a real
browser and press 「到 Klook 查看」. The new tab should be
`https://www.klook.com/destination/c28-tokyo/1-things-to-do/?aid=134379`, not a JSON error.

## Notes

- Production evidence, 2026-09-13, before the fix: the rendered form POSTed with `Origin: null` and
  no `Referer` → 403. The same button with `rel="noopener"` POSTed with
  `Origin: https://mokaair.com` → 303 to `…/c28-tokyo/1-things-to-do/?aid=134379` carrying
  `Referrer-Policy: no-referrer`, and `window.opener` stayed null. That one check wrote one
  anonymous `affiliate_clicks` row (placement `guide`, tokyo activities).
- Klook still gets no referrer: the API's 303 and the BFF's redirect both send
  `Referrer-Policy: no-referrer`, and the browser applies it to the next hop.
- Under local `next dev` the two Klook tests fail earlier, at `expect(modules).toEqual(["hotel"])`,
  because StrictMode runs the fetch effect twice. CI serves the build
  (`PLAYWRIGHT_SERVE_BUILD=true`), where the whole spec passes.
- The Claude desktop app's browser pane turns a `target="_blank"` form POST into a same-tab GET
  (405 `Method Not Allowed`). That is the pane, not the site; use Playwright for this check.
- Claimed with `--force` over `2026-09-12-trip-partner-cta`, which still says in-progress although
  it merged as #436 on 2026-09-12 with every box ticked. Only `catalog.tsx` and its test overlap.
