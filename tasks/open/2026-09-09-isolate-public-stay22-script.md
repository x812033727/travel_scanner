---
id: 2026-09-09-isolate-public-stay22-script
title: Isolate public Stay22 script document and hotel links
status: in-progress
priority: P1
area: web
owner: codex-stay22-script-ui
claimed_at: 2026-09-09T13:26:57Z
created_at: 2026-09-09T13:26:57Z
completed_at:
branch: codex/stay22-modular-toggle
depends_on: []
scope:
  - apps/web/app/[locale]/destinations/[destinationId]/services/page.tsx
  - apps/web/app/(stay22-public)
  - apps/web/components/travel-services/destination-services-page.tsx
  - apps/web/components/travel-services/stay22-public-hotels.tsx
  - apps/web/components/travel-services/stay22-public-hotels.test.tsx
  - apps/web/components/stay22-script.tsx
  - apps/web/components/stay22-script.test.tsx
  - apps/web/lib/stay22-script.ts
  - apps/web/lib/stay22-script.server.ts
  - apps/web/lib/stay22-script.server.test.ts
  - apps/web/lib/stay22-script-copy.ts
  - apps/web/lib/stay22-script.test.ts
---

# Isolate public Stay22 script document and hotel links

## Why

An official Stay22 LMA script cannot be safely treated as a disposable React
component inside the existing authenticated SPA: removing its script element does
not undo its observers, event handlers or timers. Existing booking cards are POST
forms, which are not normal external anchors for LMA to convert.

## Definition of done

- [x] Public destination hotel pages have a distinct document root when full Script
  mode is effective; leaving for the private app creates a document boundary.
- [x] Disabled, privacy-opted-out, invalid or unavailable configuration preserves
  the original page implementation and providers.
- [x] Reviewed original hotel links load only when their public platform panel is
  opened; unavailable links are never replaced with guessed search URLs.
- [ ] Coordinated production build and desktop/mobile browser boundary acceptance.

## Steps

- [x] Move the existing destination page implementation without changing its behavior.
- [x] Add exact production-host and privacy gates, bounded no-credential public
  configuration retrieval, fixed vendor script URL and validated rotatable LMA ID.
- [x] Add public hotel directory, accessible platform sheet and five-language copy.
- [x] Preserve original anchors on vendor failure and strip URL queries before
  exposing the public document to the vendor runtime.
- [x] Verify 44 focused unit tests and scoped ESLint.

## How to verify

From apps/web:

```powershell
npx vitest run lib/stay22-script.test.ts lib/stay22-script.server.test.ts components/stay22-script.test.tsx components/travel-services/stay22-public-hotels.test.tsx 'app/(stay22-public)/[locale]/layout.test.tsx'
npx eslint 'app/(stay22-public)' components/travel-services/destination-services-page.tsx components/travel-services/stay22-public-hotels.tsx components/travel-services/stay22-public-hotels.test.tsx components/stay22-script.tsx components/stay22-script.test.tsx lib/stay22-script.ts lib/stay22-script.server.ts lib/stay22-script.server.test.ts lib/stay22-script-copy.ts lib/stay22-script.test.ts --max-warnings=0
```

Both passed on 2026-09-09. Typecheck initially encountered a stale generated Next
validator referring to the moved page; regenerate/build routes before final checks.
Browser acceptance is coordinated by the root agent with a local upstream and
intercepted canonical origin; no real vendor/OTA traffic or test orders.

## Notes

- The original root globally loads Travelpayouts Drive. Script mode does not import
  its runtime providers into the rendered tree; the off branch keeps the original
  layout and original server page.
- Header session, saved items, community personalization, analytics, private dates
  and private actions are absent from the Script page. First-party public fetches
  explicitly omit credentials; this is not proof that the same-origin vendor
  script could never make its own credentialed request.
- This root separation is a document/DOM lifetime boundary, not a separate browser
  origin or cookie sandbox. Do not claim stronger isolation. Already open documents
  require reload after configuration changes; unmount does not undo vendor code.
- Full LMA seven-platform / Spark / Nova behavior comes from the reviewed Hub script;
  no undocumented controls are invented. Native application POST cards remain in
  the separate original app document and use their existing server-side strategy.
- Server activation checks only exact incoming production Host and DNT/GPC, not a
  build-inlined site URL. Browser activation independently verifies HTTPS origin.
- No active script is loaded for an incoming fragment. URL queries are redirected
  away before the script document is sent; omitting props alone would not hide them.
- Explicit non-hotel type views (including repeated conflicting query types) stay
  on the original catalogue/layout and do not load Script. This preserves tours,
  transfers, SIM and all-services links instead of silently swapping them to hotels.
- Non-catalogue destinations also retain the original affiliate-options view.
  Original destination navigation uses locale-prefixed document anchors so moving
  from a non-hotel/original view to a Script view cannot retain the old SPA layout.
- document.referrer is checked before creating the vendor global or script: only
  empty or clean exact-origin public-home/catalogue URLs are allowed. Private paths,
  query/hash, foreign origins and credentials fail closed with original-link status.
  A clean current URL alone does not hide a previous private-page referrer.
