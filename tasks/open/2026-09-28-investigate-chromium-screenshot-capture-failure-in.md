---
id: 2026-09-28-investigate-chromium-screenshot-capture-failure-in
title: Investigate Chromium screenshot capture failure in discovery UI
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-28T04:09:35Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/e2e/discovery-card-details.spec.ts
---

# Investigate Chromium screenshot capture failure in discovery UI

## Why

The desktop English discovery-card fixture failed at its full-page screenshot
with `Page.captureScreenshot: Unable to capture screenshot` in CI job
108778408030 (PR #881). Its preceding layout assertions passed and the browser
still returned a complete page snapshot. The other 502 browser tests passed
(9 skipped). The cause of this isolated capture error has not been established.

## Definition of done

- [ ] Reproduce or explain the capture failure using browser/runtime evidence.
- [ ] Preserve the existing layout assertions and required screenshots.
- [ ] Validate any justified fix on desktop/mobile light/dark discovery cases
      and the full isolated-browser CI suite, without masking failures.

## Steps

- [x] Retain the failed job log and page snapshot; compare the tested web trees.
- [ ] Capture a trace for the desktop English scenario under representative CI load.
- [ ] Check browser/rendering/resource conditions before changing test timing or code.
- [ ] Apply and validate only a fix supported by the observed cause.

## How to verify

Use the production-build setup from the web CI job, then run from apps/web:

`npx playwright test e2e/discovery-card-details.spec.ts --project=desktop-chromium -g "synthetic fixtures en" --repeat-each=20 --trace=retain-on-failure`

Keep failing archives, then run the other locales/projects and full web CI.
One successful rerun clears that run's check but does not prove a root-cause fix.

## Notes

Failure: https://github.com/x812033727/travel_scanner/actions/runs/36374827985/job/108778408030
Artifact: site-experience-browser-results (10950333718). The failed case contains
error-context.md but no trace because the suite uses on-first-retry and zero retries.
The failure is at discovery-card-details.spec.ts:176 after fonts finished loading.

PR #881 changes video-planning documents. Its failed head
bb46b5d73865f3f5d1feb4ffe8e23f7ed03bf2e7 and main d61b699290a70c6a108660eb4a2554192141e62a
have the same entire apps/web Git tree: d42c9eb126350a55b1ff6b500abade48ceb885fe.
Other PR runs with that web tree passed. PR #881 was updated from main as
independently required and is rerunning CI; no assertion, screenshot, timeout,
or retry was changed. This ticket preserves the unresolved investigation.
