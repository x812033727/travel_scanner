---
id: 2026-09-09-site-experience-settings
title: Mokaair site experience palettes and managed information pages
status: blocked
priority: P1
area: web
owner: codex-site-experience
claimed_at: 2026-09-09T10:58:26Z
created_at: 2026-09-09T10:58:08Z
completed_at:
branch: codex/site-experience-settings
depends_on: []
scope:
  - apps/api/app/site_pages
  - apps/api/app/models.py
  - apps/api/app/main.py
  - apps/api/app/i18n.py
  - apps/api/app/auth/service.py
  - apps/api/app/admin/operations_service.py
  - apps/api/migrations/versions/0069_site_pages.py
  - apps/api/tests/test_site_pages.py
  - apps/api/tests/test_site_pages_migration.py
  - apps/api/tests/test_schema.py
  - apps/api/tests/test_database_admin.py
  - apps/api/tests/support/e2e_deploy_agent.py
  - apps/web/app/[locale]/layout.tsx
  - apps/web/app/(stay22-public)/[locale]/layout.tsx
  - apps/web/app/(stay22-public)/[locale]/layout.test.tsx
  - apps/web/components/travel-services/stay22-public-hotels.tsx
  - apps/web/components/travel-services/stay22-public-hotels.test.tsx
  - apps/web/e2e/stay22-script.spec.ts
  - apps/web/app/[locale]/metadata.test.ts
  - apps/web/app/[locale]/page.test.tsx
  - apps/web/app/[locale]/pricing/page.test.tsx
  - apps/web/app/[locale]/admin/site-pages
  - apps/web/app/[locale]/privacy
  - apps/web/app/[locale]/terms
  - apps/web/app/[locale]/about
  - apps/web/app/[locale]/contact
  - apps/web/app/globals.css
  - apps/web/components/theme-provider.tsx
  - apps/web/components/flight-status-search.tsx
  - apps/web/components/date-range-picker.tsx
  - apps/web/components/hotspot-explorer.tsx
  - apps/web/components/theme-switcher.tsx
  - apps/web/components/theme-switcher.test.tsx
  - apps/web/components/palette-switcher.tsx
  - apps/web/components/palette-switcher.test.tsx
  - apps/web/components/site-header.test.tsx
  - apps/web/components/site-header.tsx
  - apps/web/components/header-session.tsx
  - apps/web/components/header-session-locale.test.tsx
  - apps/web/components/site-navigation.tsx
  - apps/web/components/site-footer.tsx
  - apps/web/components/site-footer.test.tsx
  - apps/web/components/admin-shell.tsx
  - apps/web/components/admin-nav.tsx
  - apps/web/components/discovery-navigation.test.tsx
  - apps/web/components/admin-site-pages-panel.tsx
  - apps/web/components/admin-site-pages-panel.test.tsx
  - apps/web/components/site-page-content.tsx
  - apps/web/components/site-information-page.tsx
  - apps/web/components/site-information-page.test.tsx
  - apps/web/lib/admin-operations-copy.ts
  - apps/web/components/site-page-content.test.tsx
  - apps/web/components/site-navigation.test.tsx
  - apps/web/components/community/home.tsx
  - apps/web/components/community/ui.tsx
  - apps/web/components/community/ui.test.tsx
  - apps/web/components/discovery/card.tsx
  - apps/web/components/discovery/detail-drawer.tsx
  - apps/web/components/discovery/card-details.test.tsx
  - apps/web/components/discovery/discovery.module.css
  - apps/web/components/discovery/explorer.tsx
  - apps/web/components/discovery/preferences.tsx
  - apps/web/components/discovery/discovery.test.tsx
  - apps/web/components/discovery/search-suggestions.test.tsx
  - apps/web/components/discovery/preferences.test.tsx
  - apps/web/components/discovery/frontend-flow.test.tsx
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/components/planner-overlay.tsx
  - apps/web/components/planner-overlay.test.tsx
  - apps/web/components/language-switcher.tsx
  - apps/web/components/language-switcher.test.tsx
  - apps/web/components/mobile-nav.tsx
  - apps/web/components/mobile-nav.test.tsx
  - apps/web/components/account-list.tsx
  - apps/web/components/account-list.test.tsx
  - apps/web/lib/theme.ts
  - apps/web/lib/theme.test.ts
  - apps/web/lib/palette.ts
  - apps/web/lib/palette.test.ts
  - apps/web/lib/modal-sheet.ts
  - apps/web/lib/modal-sheet.test.ts
  - apps/web/lib/modal-sheet.test.tsx
  - apps/web/lib/navigation-guard.ts
  - apps/web/lib/navigation-guard.test.ts
  - apps/web/lib/navigation-guard.test.tsx
  - apps/web/lib/navigation-history.ts
  - apps/web/lib/navigation-history.test.ts
  - apps/web/lib/frontend-flow-copy.ts
  - apps/web/lib/site-pages.ts
  - apps/web/lib/site-pages.server.ts
  - apps/web/lib/site-pages.server.test.ts
  - apps/web/lib/admin-operations.ts
  - apps/web/messages
  - apps/web/e2e/site-experience.spec.ts
  - apps/web/e2e/readability.spec.ts
  - apps/web/e2e/discovery-card-details.spec.ts
  - apps/web/e2e/site-pages.spec.ts
  - apps/web/e2e/admin-operations-full-stack.spec.ts
  - apps/web/e2e/admin-operations.spec.ts
  - apps/web/e2e/navigation.spec.ts
  - apps/web/e2e/planner-premium.spec.ts
  - tools/e2e-runtime-api.mjs
  - .github/workflows/ci.yml
  - README.md
  - docs/site-experience.md
---

# Mokaair site experience palettes and managed information pages

## Why

Implement the approved Mokaair frontend, six palettes and managed information pages plan. Preserve the original dirty checkout; work from origin/main 95122362 in an isolated worktree. Policies remain unpublished drafts. The user authorized PR #380 merge on 2026-09-09 after the incomplete manual acceptance was disclosed; deployment and policy publication remain unauthorized.

## Definition of done

- [x] All valid card topics wrap; reading links are grouped; empty detail sections disappear.
- [x] Language is reachable at the top, six palettes share state, existing planner palettes remain selectable.
- [x] Four five-language information documents support draft, preview, CAS, audited publication and revision restoration.
- [ ] Safe frontend close/back/focus flows have regression coverage and desktop/mobile browser evidence.
- [x] Relevant local checks and full CI pass; revalidate any base-branch reconciliation before the authorized merge.

## Steps

- [x] API/revisions/first drafts: hotspot_sources_kaohsiung.
- [x] Theme/root navigation: hotspot_sources_taipei.
- [x] Interaction/planner guards: archive_publication_audit.
- [x] CMS Web, discovery cards, integration, automated verification and PR: root.
- [ ] Built-in-browser manual acceptance on an approved isolated preview: root.

## How to verify

API pytest/Ruff/mypy/migration checks; Web component tests/typecheck/lint/i18n/build; scoped Playwright desktop and Pixel 7 plus built-in browser verification. Never submit production edits or paid provider actions.

## Notes

Task ownership: old review claims overlap this follow-up but their product changes are already on the verified main ancestry: PR 374 (a899437a), 375 (f6ab3d64), 378 (95122362). The task tool's explicit force option was used solely for this completed-work overlap; other owners' task records are not modified. One shared task covers the disjoint subagent file ownership above.

Initial verification: API focused 86 passed / 18 skipped (PostgreSQL-only cases require CI); root CMS/discovery 50 passed; earlier agent-focused theme and interaction suites passed apart from one subsequently fixed mobile focus regression. Production webpack build including TypeScript passed; final overlay integration changed afterward and is included in CI. Full local parallel tests were stopped because available RAM fell below 40 MB; no full-pass claim. A local preview server launch was rejected by the execution policy, so built-in browser palette evidence remains pending. No policies published, no merge or deployment.

Draft PR: https://github.com/x812033727/travel_scanner/pull/380. Follow-up evidence and exact remaining manual acceptance are recorded in docs/site-experience.md. CI-discovered strict types, managed-metadata/root-provider fixtures and admin registry navigation have been corrected. At that earlier checkpoint, current-head CI and approved-preview manual browser verification were both still open; the final code verification follows below.

Code revision 470d16d6 and the documentation-only head 552637d7 are fully green: API 2,805 passed / 15 skipped; Web units 1,445 passed; browser UI 376 passed / 4 skipped; migrations, Ruff, mypy, i18n, TypeScript, lint, build, containers, full-stack, planner and discovery workflows passed. Native multi-entry Back and the admin topbar overlap are fixed and verified. Twelve final-code palette screenshots were inspected. Main d9ef8fcd was incorporated without changing its hotel fixes.

Merge follow-up (2026-09-09): the user explicitly authorized merging PR #380. Reconcile main 73f893a2 (#383) by retaining both browser test lists and regenerating the task board; rerun CI on the combined head before a SHA-guarded merge. This task stays blocked only on the outstanding built-in-browser manual acceptance: an approved isolated preview URL is still needed after local preview startup was rejected by execution policy. No alternative launcher, deployment, policy publication or production mutation is authorized by this merge request. Automatic browser evidence is not a substitute for that manual checklist.
