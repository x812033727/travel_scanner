---
id: 2026-09-08-travel-discovery-integration
title: Travel discovery integration navigation safety and acceptance
status: in-progress
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

- [ ] Default-off homepage/discovery and four-destination navigation preserve old mode.
- [ ] Public curated reads and private actions remain safe through the BFF.
- [ ] Aggregate search and useful-action metrics preserve existing analytics consent;
  unavailable cross-day member retention is not misrepresented as zero.
- [ ] Desktop/Pixel 7 acceptance, full regressions, migrations and CI validated.
- [ ] Documentation, source/usage boundaries and PR handoff complete without deployment.

## Steps

- [x] Create isolated branch from main 29c36b2 and import task-only Klook archive.
- [x] Claim bounded backend/community/Web tasks and coordinate active planner owner.
- [ ] Integrate feature-gated navigation, video CSP, BFF and browser tests.
- [ ] Verify full implementation and prepare evidence-backed PR, no merge authorization.

## How to verify

Run tools/tasks, Ruff, mypy, pytest, migrations, Web lint/typecheck/Vitest/build;
run new isolated and full-stack browser cases on desktop and Pixel 7. No paid
queries or writes to production. Existing planner tests remain owned by PR #371.

## Notes

Planner owner confirms it holds only global CSS and planner-specific files, not
home/explore/nav/saved. Do not change globals.css or its E2E suites. Stay22 owner
explicitly released only csp.ts/csp.test.ts after confirming no undelivered work;
the narrow task-only handoff is recorded without importing unverified planner code.
