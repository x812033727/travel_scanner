---
id: 2026-10-04-show-site-context-and-real-articles
title: Show site context and real articles before homepage discovery
status: done
priority: P1
area: web
owner: codex-gpt6-home
claimed_at: 2026-10-04T08:09:53Z
created_at: 2026-10-04T08:09:42Z
completed_at: 2026-10-04T08:20:04Z
branch: codex/adsense-content-fixes-20261004
depends_on: []
scope:
  - apps/web/app/[locale]/page.tsx
  - apps/web/app/[locale]/page.test.tsx
  - apps/web/components/home-guides.tsx
  - apps/web/components/home-guides.test.tsx
---

# Show site context and real articles before homepage discovery

## Why

On the current homepage, twenty discovery cards precede the site introduction and the
travel, technology and money article links. Readers should understand what Mokaair covers
and reach substantive articles before that feed. Google reports low-value content without
identifying specific URLs; this change improves the observed homepage ordering and does
not claim to resolve every review concern or guarantee approval.

## Definition of done

- [x] The site introduction and the existing three article groups appear before discovery
      cards in the server-rendered HTML, with up to four real article links per group.
- [x] A direct trip-search link is available near the introduction; discovery off and an
      unavailable feed retain the full original search form and destination entrances.
- [x] An empty article response keeps the introduction and omits empty groups.
- [x] Focused single-worker tests cover the meaningful ordering and fallback behavior.

## Steps

- [x] Read apps/web/AGENTS.md, local Next Server and Client Components docs, task-board,
      dev-and-ci and web-i18n-e2e; claim exactly the four permitted homepage files.
- [x] Add server-HTML order regressions for discovery off/on and feed failure.
- [x] Move the article introduction ahead of the gate and preserve search access.
- [x] Run focused checks and hand the changes to the parent agent for integration.

## How to verify

Use the verified bundled Node 24.19 runtime in apps/web:
`node ../../node_modules/vitest/vitest.mjs run "app/[locale]/page.test.tsx" components/home-guides.test.tsx --maxWorkers=1`.
The parent agent handles broader validation and CI. Do not install dependencies, start
servers, use browsers, SSH, change production settings, commit or push for this subtask.

## Notes

- Shared branch: `codex/adsense-review-audit-20261004`; owner: `codex-gpt6-home`.
- Existing article requests use `sort=curated`, which ranks featured and display order
  before publication time. Retain that request and the neutral topic headings; do not
  claim every returned row is editorially selected, or change publication dates.
- Reuse the existing five-language `getFrontendFlowCopy(locale).searchTrips` label;
  no message catalog edits or new display strings are needed.
- `HomeGuides` remains outside the client discovery gate so both server rendering and
  later client switch resolution preserve the introduction and article links.
- 2026-10-04: `HomeGuides` now precedes the gate. Its three topic groups use a desktop
  three-column layout and a stacked mobile layout, with the unchanged compact article
  summaries. The introduction carries an immediate `/search/new` link even when the
  original full search form is farther down the discovery-off page.
- Red verification on the old page order: 4 of 5 page tests failed at the intended DOM
  ordering assertion (`DOCUMENT_POSITION_FOLLOWING` was 0), covering empty article
  reads and server HTML with discovery off, on, and an unavailable feed.
- Green verification with bundled Node v24.19.0 and Vitest v5.0.2, one worker:
  `app/[locale]/page.test.tsx` plus `components/home-guides.test.tsx`: 2 files / 7 tests
  passed, exit 0. The SSR cases use the real discovery gate and explorer, twenty feed
  cards and twelve actual article links/descriptions, without component hydration.
- Targeted ESLint for all four source/test files passed with `--max-warnings=0`, exit 0;
  `git diff --check` passed. No npm install, full suite, browser, server, SSH, production
  change, commit or push. Parent agent owns broader validation, PR and deployment.
