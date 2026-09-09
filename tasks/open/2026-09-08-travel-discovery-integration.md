---
id: 2026-09-08-travel-discovery-integration
title: Travel discovery integration navigation safety and acceptance
status: review
priority: P1
area: web
owner: codex-discovery-root
claimed_at: 2026-09-09T00:02:51Z
created_at: 2026-09-08T23:24:12Z
completed_at:
branch: codex/travel-discovery-community
depends_on: []
scope:
  - docs/travel-discovery.md
  - apps/web/e2e/discovery.spec.ts
  - apps/web/e2e/discovery-full-stack.spec.ts
  - apps/web/app/api/travel
  - .env.example
  - apps/web/components/site-navigation.tsx
  - apps/web/components/site-navigation.test.tsx
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/app-bottom-nav.tsx
  - apps/web/components/discovery-navigation.test.tsx
  - .github/workflows/travel-discovery.yml
  - apps/web/lib/csp.ts
  - apps/web/lib/csp.test.ts
  - apps/api/app/i18n.py
  - apps/api/app/analytics/service.py
  - apps/api/app/analytics/discovery.py
  - apps/api/tests/test_discovery_metrics.py
---

# Travel discovery integration navigation safety and acceptance

## Why

Integrate the approved travel-search and social discovery plan in an isolated
worktree without changing existing itinerary work, production gates or paid services.

## Definition of done

- [x] Default-off homepage/discovery and four-destination navigation preserve old mode.
- [x] Public curated reads and private actions remain safe through the BFF.
- [x] Aggregate search and useful-action metrics preserve existing analytics consent;
  unavailable cross-day member retention is not misrepresented as zero.
- [ ] Desktop/Pixel 7 acceptance, full regressions, migrations and CI validated.
- [ ] Documentation, source/usage boundaries and PR handoff complete without deployment.

## Steps

- [x] Create isolated branch from main 29c36b2 and import task-only Klook archive.
- [x] Claim bounded backend/community/Web tasks and coordinate active planner owner.
- [x] Integrate feature-gated navigation, video CSP, BFF and browser tests.
- [ ] Verify full implementation and prepare evidence-backed PR, no merge authorization.

## How to verify

Run tools/tasks, Ruff, mypy, pytest, migrations, Web lint/typecheck/Vitest/build;
run new isolated and full-stack browser cases on desktop and Pixel 7. No paid
queries or writes to production. The planner source from merged PR #371 stays
unchanged; the Web integration task claims the exact strict planner fixture for
the new read-only discovery-status response.

## Notes

Planner owner originally held only global CSS and planner-specific files, not
home/explore/nav/saved. Do not change globals.css. After its completion archive,
the Web task claimed the exact planner E2E fixture for status-query compatibility. Stay22 owner
explicitly released only csp.ts/csp.test.ts after confirming no undelivered work;
the narrow task-only handoff is recorded without importing unverified planner code.

Rebased application work cleanly onto main f752ce43 after planner PR #371 merged.
Only generated task-board conflicts needed regeneration. The obsolete narrow
Stay22 scope commit was dropped because main already contains the owner's full
archive; the subsequent owner-authorized task-only planner completion record was
imported separately. No source edits to the user's original checkout.

Local validation after rebase: Ruff, mypy (275 files), pytest 2018 passed / 125
integration skips. Only Windows-incompatible deployment-agent tests were excluded;
Linux CI executes them and PostgreSQL/Redis/S3 integration. Existing AsyncMock warning
in test_usage_settings remains. Web lint/typecheck and production build passed;
metadata + feature regressions 99 passed; nav/BFF/CSP regressions 22 passed. First
whole Web run found metadata and one shared-Response fixture defect, now fixed.
Desktop/Pixel 7 focus/search/legacy-hub recheck passed all 6 focused cases; final
whole enabled-feature browser and Linux full-stack runs remain release gates.

PR: https://github.com/x812033727/travel_scanner/pull/372 (draft until final CI).
Final local production-browser run: all 18 discovery cases passed on desktop and
Pixel 7. Reviewed Traditional-Chinese desktop/mobile and dark video screenshots;
mobile filters collapse by default and all four bottom destinations remain visible.
Linux enabled-discovery workflow passed on fa280c3a; ordinary login, verification,
invited moderation, private collections and withdrawal ran against real services.
Core full-stack smoke also passed. Planner regression exposed only a missing mock
for the new public status endpoint, assigned to the Web task without weakening its
unexpected-request or mutation assertions. Final head CI is tracked in the PR.
No merge, deployment, production activation or provider call was authorized.
