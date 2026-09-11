---
id: 2026-09-09-verify-stay22-script-browser
title: Verify isolated Stay22 Script public browser flow
status: done
priority: P1
area: web
owner: codex-stay22-script-e2e
claimed_at: 2026-09-09T13:32:33Z
created_at: 2026-09-09T13:32:11Z
completed_at: 2026-09-11T15:54:20Z
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

PR CI follow-up: run 34360841653 / web job 102497095957 had one mobile failure
because the conflicting-category test expected the initial duplicate query to stay
unchanged after hydration. The original DestinationServices component treats the
repeated type array as no valid initial category; ServiceCatalog's existing filter
effect selects all and deletes type through history.replaceState. It does not
navigate, redirect or enable Script. The same-head push suite passed, exposing the
old test's pre-/post-hydration assertion race rather than a provider regression.

The corrected test positively verifies valid tour selection and its preserved URL;
for duplicate categories it verifies local HTTP 200, no redirect, original shell,
no SDK/config request, then the hydrated clean URL, selected all category and still
no Script. Scoped ESLint passed. Desktop Chromium and Pixel 7 each repeated the
corrected case five times: 10 passed in 40.9 seconds, workers=1, unchanged production
build and offline transport guard. The parent owns the follow-up CI; the combined
50-case regression is rerun after the evidence handoff and reported on PR #383.

## Closed after merge (site owner's instruction, not the holder)

PR #383 merged on 2026-09-09 as squash `73f893a`, whose tree is identical to the PR head
`132e3d7`, so everything on the branch reached main; the branch has since been deleted.
Every check on that head passed: `api`, `web`, `containers`, `full-stack-smoke`,
`discovery-browser` and `planner-browser`. The task stayed in `review` and kept holding its
scope, which blocked later claims, so claude-opus-5 moved it to done on 2026-09-11.

If the holder still has follow-up work that never reached the branch, file a new task rather
than reopening this one.
