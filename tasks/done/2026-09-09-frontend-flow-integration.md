---
id: 2026-09-09-frontend-flow-integration
title: Frontend flow navigation planning handoff and acceptance
status: done
priority: P1
area: web
owner: codex-frontend-flow
claimed_at: 2026-09-09T03:08:42Z
created_at: 2026-09-09T03:06:54Z
completed_at: 2026-09-10T03:28:33Z
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
  - apps/web/components/community/ui.tsx
  - apps/web/components/community/ui.test.tsx
  - apps/web/components/search-workbench.tsx
  - apps/web/components/search-workbench.test.tsx
  - apps/web/app/[locale]/search/new
  - apps/web/messages/en/metadata.json
  - apps/web/messages/ja/metadata.json
  - apps/web/messages/ko/metadata.json
  - apps/web/messages/zh-TW/metadata.json
  - apps/web/messages/zh-CN/metadata.json
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
---

# Frontend flow navigation planning handoff and acceptance

## Why

Make the approved explore → save → trip journey calm and continuous, without replacing the existing planner or publishing changes to production.

## Definition of done

- [x] Four consistent navigation destinations, optional search form, contextual planning and safe new-trip handoff.
- [ ] Five languages, accessible desktop/mobile and dark mode; regression tests and full-stack acceptance.
- [ ] PR #374 with verified checks; merge and deployment remain separately authorized.

## Steps

- [x] Implement navigation, My directory and standalone search form.
- [x] Integrate shared save and contextual trip selection, retaining creation recovery.
- [ ] Exercise fixture and full-stack scenarios, document evidence and open PR.

## How to verify

Run web lint/i18n/types/Vitest/build, API Ruff/mypy/pytest/migration, desktop and Pixel 7 Playwright. Production inspection is read-only.

## Notes

- 2026-09-09 scope handoff: original coordinator confirmed source work stopped and released .github/workflows/travel-discovery.yml to 2026-09-09-discovery-card-details only to include its additional browser suite; all existing suites must remain. Other scope, owner and review status remain unchanged.

Base main 7cee8650 includes planner PR #373. Owner authorized task-only closure dcc97fbd, imported as f7b78cc, and released new-trip-form for a minimal success handoff. No itinerary timeline/draft behavior changes.

CI acceptance surfaced native nested dialog cancel/close propagation and a new-trip mobile navigation overlap. Both are fixed without weakening Escape assertions; 12 focused dialog/navigation tests pass. The standalone search metadata follows all five existing locale catalogs; 41 metadata tests and i18n checks pass. TypeScript passed after regenerating a corrupted local development type cache. Discovery desktop/Pixel 7 five-language editorial screenshots pass and are retained as explicitly synthetic fixture renders. Complete rerun remains required before review handoff.

PR: https://github.com/x812033727/travel_scanner/pull/374. Review status means the PR is open; it is not merge/deployment authorization or a claim that pending CI is complete. The current PR checks remain the authoritative final acceptance record.

2026-09-09 merge/deploy follow-up: user explicitly authorized merge and deployment, including the approved Discovery ON / Community OFF release behavior. Integrated main f6ab3d64 (PR #375) without dropping planner fixes. All integration checks passed except one mobile navigation strict-locator failure: the visitor fare-lab login CTA shared a substring with the new account login link. Add exact accessible-name matching to the test, retaining its return-path and no-charge-button assertions; this is not a product/auth change. Re-run final-head CI before merging and keep the production environment unchanged until backup and release checks pass.
