---
id: 2026-09-09-frontend-flow-integration
title: Frontend flow navigation planning handoff and acceptance
status: in-progress
priority: P1
area: web
owner: codex-frontend-flow
claimed_at: 2026-09-09T03:08:42Z
created_at: 2026-09-09T03:06:54Z
completed_at:
branch: codex/frontend-explore-flow
depends_on: []
scope:
  - apps/web/components/site-navigation.tsx
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/mobile-nav.test.tsx
  - apps/web/components/app-bottom-nav.tsx
  - apps/web/components/app-bottom-nav.test.tsx
  - apps/web/components/site-navigation.test.tsx
  - apps/web/components/community/home.tsx
  - apps/web/components/search-workbench.tsx
  - apps/web/components/search-workbench.test.tsx
  - apps/web/app/[locale]/search/new
  - apps/web/components/account-list.tsx
  - apps/web/components/account-list.test.tsx
  - apps/web/components/travel-card-actions.tsx
  - apps/web/components/travel-card-actions.test.tsx
  - apps/web/components/new-trip-form.tsx
  - apps/web/components/new-trip-form.test.tsx
  - apps/web/components/new-trip-auth-gate.tsx
  - apps/web/components/new-trip-auth-gate.test.tsx
  - apps/web/app/[locale]/trips/new/page.tsx
  - apps/web/components/travel-services/catalog.tsx
  - apps/web/components/travel-services/catalog.test.tsx
  - apps/web/lib/frontend-flow.ts
  - apps/web/lib/frontend-flow.test.ts
  - apps/web/lib/frontend-navigation.ts
  - apps/web/app/globals.css
  - apps/web/e2e/frontend-flow.spec.ts
  - apps/web/e2e/frontend-flow-full-stack.spec.ts
  - apps/web/playwright.frontend-flow.config.ts
  - docs/frontend-flow.md
  - .github/workflows/travel-discovery.yml
---

# Frontend flow navigation planning handoff and acceptance

## Why

Make the approved explore → save → trip journey calm and continuous, without replacing the existing planner or publishing changes to production.

## Definition of done

- [ ] Four consistent navigation destinations, optional search form, contextual planning and safe new-trip handoff.
- [ ] Five languages, accessible desktop/mobile and dark mode; regression tests and full-stack acceptance.
- [ ] PR with verified checks; merge and deployment remain separately authorized.

## Steps

- [ ] Implement navigation, My directory and standalone search form.
- [ ] Integrate shared save and contextual trip selection, retaining creation recovery.
- [ ] Exercise fixture and full-stack scenarios, document evidence and open PR.

## How to verify

Run web lint/i18n/types/Vitest/build, API Ruff/mypy/pytest/migration, desktop and Pixel 7 Playwright. Production inspection is read-only.

## Notes

Base main 7cee8650 includes planner PR #373. Owner authorized task-only closure dcc97fbd, imported as f7b78cc, and released new-trip-form for a minimal success handoff. No itinerary timeline/draft behavior changes.
