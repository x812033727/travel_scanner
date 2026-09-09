---
id: 2026-09-09-discovery-card-details
title: Compact discovery cards and source-linked details
status: review
priority: P2
area: web
owner: codex-discovery-card-details
claimed_at: 2026-09-09T09:27:48Z
created_at: 2026-09-09T09:24:00Z
completed_at:
branch: codex/discovery-card-details-20260909
depends_on: []
scope:
  - apps/api/app/discovery
  - apps/api/tests/test_discovery_display_topics.py
  - apps/web/components/discovery/card.tsx
  - apps/web/components/discovery/discovery.module.css
  - apps/web/components/discovery/frontend-flow.test.tsx
  - apps/web/components/discovery/card-details.test.tsx
  - apps/web/lib/discovery.ts
  - apps/web/e2e/discovery-card-details.spec.ts
  - .github/workflows/travel-discovery.yml
---

# Compact discovery cards and source-linked details

## Why

Discovery details repeat raw coordinates and route related reading through another drawer. Text-only cards waste space on type placeholders and omit existing localized categories and reviewed themes.

## Definition of done

- [x] Details omit coordinates/copy but preserve maps, attribution and planning data; related guides link safely to their original source in a new tab with a source label.
- [x] Cards preserve authorized images, remove no-image placeholders and display at most two localized distinct topics with a remaining count.
- [x] API adds a backward-compatible display_topics projection, batching enabled hotspot themes and approved merchant styles without changing filtering/publication.
- [ ] Scoped API/Web tests, five-language checks, lint/types/build and desktop/Pixel 7 browser fixtures pass; record any environment gaps.

## Steps

- [x] Verify fresh main, establish isolated worktree and coordinate original scope release.
- [x] Implement API projection and frontend presentation with regression tests.
- [ ] Validate final diff and open a PR without merging or deploying.

## How to verify

Run API Ruff/mypy and pytest including test_discovery_display_topics.py, test_discovery_flow.py and test_travel_discovery.py. Run npm lint:web/check:i18n/typecheck:web/test:web/build:web/test:tools/check:tasks. Run Playwright discovery-card-details.spec.ts plus existing discovery.spec.ts and frontend-flow.spec.ts against the production build on desktop and Pixel 7.

## Notes

- Base: main 59c86438e3100129bbff554f9dce3df95e25a2ac; original dirty worktree untouched. No migrations, provider requests, feature activation, merge or deployment.
- Original PR #374 coordinator (task 01a057d3-8adc-7d21-9285-4dfddd5533da) explicitly confirmed frozen source and authorized the limited scope-release metadata synchronization on 2026-09-09. Existing task owner/status and all prior CI suites are retained.
- Before changes: 24 discovery API tests and 28 discovery Web tests passed; Ruff, mypy (288 files), TypeScript and five-language namespace check passed. Docker is unavailable locally; PostgreSQL/container validation will use CI.
- Post-change scoped API: 85 passed / 3 PostgreSQL-only skips; Ruff passed, mypy passed 289 files. Full local API: 2,265 passed / 139 environment skips / one unrelated disk-capacity-dependent backup test failure, also reproduced on untouched base; filed 2026-09-09-backup-catalog-free-disk-fixture rather than changing deployment safety.
- Web lint, TypeScript, five locales across 25 namespaces, repository task checks and all 27 tool tests passed. Production build passed with 267 generated pages. Independent frontend/API static reviews found no actionable defects.
- Production-build browser fixtures: all 46 enabled cases passed across desktop and Pixel 7; two opt-in production baseline captures intentionally skipped. Includes all 14 new cases, five locales, light/dark/large text, long topic wrapping, keyboard focus return, direct safe source popups, no-coordinate display and image authorization paths. Viewed desktop/mobile screenshots; evidence is synthetic local fixtures, not production or provider-licensing evidence. Screenshots remain in apps/web/test-results/discovery-card-details.
- Scoped Web initially passed 53 tests; added legacy-null source-label regression and reran the complete admin-settings-panel suite plus new card suite: all 71 passed. A concurrent full Web run reported one existing admin Back/Forward focus wait failure under build load; that unchanged 45-test admin suite passed in the isolated rerun. Full Web/CI results are still pending at PR creation.
