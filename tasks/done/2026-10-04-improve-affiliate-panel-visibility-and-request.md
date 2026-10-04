---
id: 2026-10-04-improve-affiliate-panel-visibility-and-request
title: Improve affiliate panel visibility and request context
status: done
priority: P2
area: web
owner: codex-monetization
claimed_at: 2026-10-04T05:53:33Z
created_at: 2026-10-04T05:53:32Z
completed_at: 2026-10-04T06:17:03Z
branch: codex/frontend-monetization-20261004
depends_on: []
scope:
  - apps/web/components/destination-affiliate-options.tsx
  - apps/web/components/destination-affiliate-options.test.tsx
  - apps/web/components/affiliate-partner-options.tsx
  - apps/web/components/affiliate-partner-options.test.tsx
  - apps/web/app/api/travel/[...path]/route.ts
  - apps/web/app/api/travel/[...path]/route.test.ts
---

# Improve affiliate panel visibility and request context

## Why

On narrow screens, horizontal partner rails hide later booking choices. Search/trip
panels can retain the previous source's options while a new lookup is pending, and
form clickouts do not consistently carry the locale of the tab that was clicked.
Below-fold destination panels also start all category queries during initial load.

## Definition of done

- [x] Every partner choice is visible and long translated labels wrap on phones.
- [x] Changed or invalid source inputs cannot show stale partner buttons; obsolete requests abort.
- [x] Both form variants preserve the clicked tab's locale through the BFF while retaining token, placement and article attribution.
- [x] Destination lookups start near the viewport, fall back without IntersectionObserver and render no empty card when offers are unavailable.

## Steps

- [x] Update the two panels without changing partner order, eligibility or enable switches.
- [x] Extend the existing BFF locale handling to generic partner clickout forms.
- [x] Verify request cancellation, locales, article attribution, empty states and viewport gating.

## How to verify

Run the affected Vitest component and BFF suites, then web lint, i18n, typecheck,
web tests and task checks. Check the mobile layout with multiple long CTAs.

## Notes

- 2026-10-04: read-only production config returned ads enabled and CMP enabled;
  Tokyo activity destination offers returned a Klook entry. No production write,
  partner click, approval, booking or revenue verification is part of this change.
- Locale query support already exists for destination/offer/hotel forms. Generic
  `/affiliates/<partner>/clickout` needs the same narrowly scoped BFF handling.
- Focused Vitest: 3 files, 38 tests passed using bundled Node 24.19.0. Full web
  lint, five-locale i18n and TypeScript checks passed; task and whitespace checks passed.
- Browser check with a local fixture (no third-party click): at 390px width,
  document width was 375px and three long-CTA buttons stayed within the viewport;
  heights were 45.3, 65.3 and 85.3px, with no internal horizontal overflow.
  At 1280px the same choices formed two columns and long text wrapped.
- Viewport margin is 1,200px before the panel. No measured production CLS guarantee
  is claimed: slow networks or fast scrolling can still reveal a late-loaded panel.
- Generic partner SubID remains the value held in the server token from the listing
  request; locale forwarding does not re-sign or rewrite that existing token.
- Full npm run test:web was attempted with Node 24.19.0 but stopped after about
  14 minutes without a completed-file report. Host free physical memory was about
  536 MiB; extreme paging is plausible but no root cause or full-suite pass is claimed.
  The retained log is in the local temp directory as
  mokaair-monetization-web-tests-20261004.log. Draft PR CI must cover the full suite.
- An unrelated development-tool braces advisory was filed in
  2026-10-04-investigate-braces-advisory-in-the-next and released; no dependency
  version was changed. Production-only npm audit reported zero vulnerabilities.
