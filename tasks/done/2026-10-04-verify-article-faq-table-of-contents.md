---
id: 2026-10-04-verify-article-faq-table-of-contents
title: Verify article FAQ table of contents in desktop and mobile reading flows
status: done
priority: P1
area: web
owner: codex-gpt6-browser
claimed_at: 2026-10-04T08:17:23Z
created_at: 2026-10-04T08:17:12Z
completed_at: 2026-10-04T08:44:59Z
branch: codex/adsense-content-fixes-20261004
depends_on: []
scope:
  - apps/web/e2e/guides-adsense.spec.ts
---

# Verify article FAQ table of contents in desktop and mobile reading flows

## Why

A published article's contents link reached a leftover FAQ heading while its
answers appeared after recommendations. Unit coverage needs a real Next/browser
reading flow that exercises hash navigation, opening answers and small screens.

## Definition of done

- [x] The authored FAQ contents link reaches the heading adjacent to its answers.
- [x] Multiple FAQ groups precede related reading and remain readable on desktop/mobile.

## Steps

- [x] Add synthetic FAQ/related-reading data to the existing isolated AdSense fixture.
- [x] Run the targeted regression in both configured browser projects and record evidence.

## How to verify

After building the current web tree, run `playwright test e2e/guides-adsense.spec.ts
-g "FAQ contents links" --workers=1`. The isolated fixture blocks external requests,
uses a synthetic publisher, and disables ads for the FAQ navigation case.

## Notes

2026-10-04: fixture uses an authored non-generic FAQ heading, a second unheaded FAQ,
three H2 sections and a related article. Assertions inspect the hash target, actual
opened answers, document order and main-content width. Existing workflow already
enumerates this spec; no new test file/workflow entry is needed.

2026-10-04 integration: Node v24.19.0 `next build --webpack` completed, exit 0.
Against that build, the targeted isolated regression passed desktop-chromium and
mobile-chromium: 2 passed (13.8s), exit 0. The assertions exercised the authored
hash target, adjacent questions, both opened answers, FAQ groups before related
reading and the mobile content width. Logs are preserved under
`<home>/mokaair-work/adsense-review-20261004/`. This is synthetic local
browser evidence; no production deployment or AdSense approval is implied.
