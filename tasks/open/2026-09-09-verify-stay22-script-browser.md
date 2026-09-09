---
id: 2026-09-09-verify-stay22-script-browser
title: Verify isolated Stay22 Script public browser flow
status: review
priority: P1
area: web
owner: codex-stay22-script-e2e
claimed_at: 2026-09-09T13:32:33Z
created_at: 2026-09-09T13:32:11Z
completed_at:
branch: codex/stay22-modular-toggle
depends_on: []
scope:
  - apps/web/e2e/stay22-script.spec.ts
---

# Verify isolated Stay22 Script public browser flow

## Why

The optional full Stay22 Script must remain confined to the approved public hotel
document, preserve reviewed originals if it cannot load, and never run on private,
preview or privacy-opted-out visits. Static/unit fixtures alone do not prove root
layout boundaries, hostname checks or dynamically opened booking sheets.

## Definition of done

- [x] Mock SDK sees reviewed native anchors after opening/reopening the booking sheet without Allez double-wrapping.
- [x] Off/error/invalid configuration, DNT/GPC and localhost/preview fail closed.
- [x] Public-to-private document navigation clears vendor state; back navigation is usable.
- [x] Desktop and Pixel 7 have usable modal focus/touch sizes, no horizontal overflow or unexpected errors.

## Steps

- [x] Add isolated loopback API/production Next and fully intercepted canonical browser origin.
- [x] Run build-coordinated browser suite and resolve real regressions with owning agents.

## How to verify

After next build: PLAYWRIGHT_SERVE_BUILD=true npm run test:e2e --workspace
@travel-scanner/web -- stay22-script.spec.ts --workers=1. Root owns the CI command
update to include this new spec. All SDK and popup responses are synthetic; browser
canonical URLs are routed locally, and unrecognized external hosts are aborted.

## Notes

No production bypass flag, external SDK download or live affiliate click is used.
Primary source code is owned by the architecture/backend agents; this task owns only
the new test file. Integration must await the root's coordinated production build.

Initial browser run exposed a test-transport limitation: a fulfilled canonical
HTTP redirect can bypass Playwright routing. Four query/mode-change cases may have
made unintended read-only production requests; their fallback page content did not
match the local fixtures. Do not describe that initial run as zero-network. No live
hotel/affiliate target was clicked. The repaired harness forces browser offline
mode and proves it with an un-intercepted reserved .invalid canary; all intended
requests are fulfilled through Node's loopback transport. Query redirects are
asserted via local HTTP with redirects disabled, then their clean target is opened
separately. It also closes browser contexts before stopping the fixture server,
avoiding ECONNRESET from in-flight legacy navigation prefetch during teardown.

Final repaired-harness validation (2026-09-09): scoped ESLint passed; the shared
production build completed before the browser run (no test-specific rebuild).
PLAYWRIGHT_SERVE_BUILD=true, PLAYWRIGHT_PORT=3315 and workers=1 ran
stay22-script.spec.ts together with stay22-allez.spec.ts: 50 passed in 1.9 minutes
(28 new Script scenarios plus 22 existing Allez scenarios across desktop Chromium
and Pixel 7). Every new Script browser context used offline mode and verified
ERR_INTERNET_DISCONNECTED for the reserved .invalid canary. The successful run does
not validate a browser-followed HTTP redirect chain, actual vendor SDK behavior,
partner attribution, commissions, or live platform availability.

Synthetic visual evidence is retained locally under apps/web/test-results in the
desktop-chromium and mobile-chromium directories for the public Script
double-wrapping scenario, each named stay22-script-public-panel.png. These show the
mock-SDK platform sheet, not real Stay22 or Booking inventory. The parent reviewed
the desktop/mobile panel presentation; browser assertions also verified sheet
focus, touch targets, original/rewritten link behavior and viewport bounds.
