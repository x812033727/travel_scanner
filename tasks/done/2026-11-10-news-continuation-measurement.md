---
id: 2026-11-10-news-continuation-measurement
title: Improve news continuation and content click measurement
status: done
priority: P1
area: web
owner: codex-news-continuation
claimed_at: 2026-11-10T12:49:29Z
created_at: 2026-11-10T12:49:28Z
completed_at: 2026-11-10T13:27:41Z
branch: codex/mokaair-news-layout-20261110
depends_on: []
scope:
  - apps/web/components/guides/related-grid.tsx
  - apps/web/components/guides/related-grid.test.tsx
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article.test.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/guides/article-page.test.tsx
  - apps/web/lib/analytics.ts
  - apps/web/components/analytics-provider.tsx
  - apps/web/components/analytics-provider.test.tsx
  - apps/web/lib/content-analytics.ts
  - apps/web/lib/content-analytics-messages
  - apps/web/components/admin-content-analytics.tsx
  - apps/web/components/admin-content-analytics.test.tsx
  - apps/web/components/admin-analytics-panel.tsx
  - apps/web/components/admin-analytics-panel.test.tsx
  - apps/api/app/analytics/schemas.py
  - apps/api/app/analytics/service.py
  - apps/api/app/analytics/router.py
  - apps/api/app/analytics/content.py
  - apps/api/tests/test_content_analytics.py
  - apps/api/tests/test_content_analytics_integration.py
  - apps/api/tests/test_analytics.py
  - apps/api/tests/test_analytics_events.py
  - apps/api/tests/test_analytics_integration.py
  - apps/web/e2e/guides-adsense.spec.ts
  - apps/web/e2e/admin-analytics.spec.ts
  - docs/news-reader-enhancements/reading-and-measurement.md
---

# Improve news continuation and content click measurement

## Why

Readers can already reach published related articles and topic hubs, but the next step is
easy to miss and ordinary internal clicks have no first-party measurement. Preserve the
editorial layout in PR #2061 while making those paths clear and reporting actual continuation
clicks in the existing analytics workspace. A click is not an impression, completed read,
search conversion or revenue.

## Definition of done

- [x] Related reading has a clear next step and topic links use their canonical hubs.
- [x] Published continuation links remain useful without JavaScript or analytics availability.
- [x] Content clicks are typed, privacy-gated and sent only after API capability confirmation.
- [x] The existing admin analytics page displays a separately degradable continuation-click
  section with a truthful raw-data window; it does not invent a 12-month history or CTR.
- [x] Five-language copy, browser navigation and PostgreSQL ingestion/aggregation are covered.
- [x] Root and independent review complete before any push/merge/deployment decision.

## Steps

- [x] Read current ownership, layout lineage and existing analytics/guide contracts.
- [x] Implement canonical continuation links and typed browser measurement.
- [x] Implement capability, strict ingestion fields and bounded content aggregation API.
- [x] Add the isolated admin section with dedicated five-language messages.
- [x] Add targeted unit, integration and browser regressions; run appropriate checks.
- [x] Document results, limitations and independent review.

## How to verify

Use the worktree's installed dependencies and bundled Node. Run focused Vitest cases for
related-grid/article/provider/admin-content-analytics, the existing guides-adsense and
admin-analytics Playwright specs, web lint/typecheck/i18n, and API ruff/mypy plus
test_content_analytics*, test_analytics*. PostgreSQL cases require RUN_INTEGRATION_TESTS=1;
report skips explicitly. Verify new-event capability absence, DNT/GPC/disabled/private
gates, rejected unsafe targets, duplicate event IDs, source/target counts and zero-history
states. Keep unrelated existing dashboard and affiliate behavior intact.

## Notes

- Root authorized this scoped implementation on 2026-11-10; no commit/push/production actions.
- Base: PR #2061 at 398fd3f77313b24fb547f09f95b026f25a54f442. Do not start from the
  docs-only #2063 worktree, which lacks this layout.
- Existing related references are publication-aware and both news and tutorials can be
  kind=life; do not relabel every related article as a tutorial.
- New events are first-party only. Keep GA4 denied defaults and all current opt-out gates.
- No models, migration, scheduler, body-inline tracking or shared E2E runtime API changes.
- Use a dedicated content-analytics message catalog to avoid other tasks' admin.json scope.

## Validation so far

- API focused tests: 30 passed, 1 PostgreSQL integration skipped (services not yet run), exit 0.
- API focused ruff and mypy: exit 0.
- Web focused Vitest: 118 passed across 6 files, exit 0.
- Web focused ESLint and full typecheck: exit 0.
- New browser cases cover non-blocking keyboard continuation with a held analytics response,
  old-API capability absence, five-language admin counts, narrow widths and report failure.
- PostgreSQL and production-build browser checks remain pending root-coordinated execution.
- Local evidence is under <home>/.codex/tmp/mokaair-news-upgrade-20261110/; initial failed
  test/lint logs are retained alongside corrected passes. No merge, deploy or production data writes.
## Final browser and database checks

- Production `next build --webpack`: exit 0; compilation, full TypeScript and 371 static
  pages completed. New topic Atom route is present in the build.
- guides-adsense Playwright: 38/38 passed across desktop/mobile, exit 0.
- admin-analytics Playwright: 16/16 passed across desktop/mobile, including all five locales,
  320/390 widths, unavailable 12-month reporting and independent report failure, exit 0.
- The first admin browser collection failed on Node ESM importing JSON without an import
  attribute; the owned spec now reads its JSON fixture catalogs using node:fs. The revised
  spec lint and browser run passed; the original failure log is retained.
- Real PostgreSQL/Redis integration, executed serially by root against the new local test
  database: 1 passed in 13.76s, exit 0 (`analytics-integration.log`). It verifies the stored
  typed JSON, UUID replay handling, DNT/GPC rejection and exact SQL grouping.
- Independent second-eye review by codex-layout-review found no blocking issues in privacy,
  capability negotiation, strict payload/route gates, report semantics or degraded UI.
- Root separately reports full API ruff, app/tests mypy, full web lint and i18n passed.
- First visual run: 34 rendered pages, 46 PNGs, 8 real Atom responses, no page errors.
  A final pass is adding horizontal-end/clipboard evidence and a complete affiliate fixture.
## Final visual verification

- Final isolated production-build capture exited 0: 35 rendered pages, 63 PNGs, 8 actual
  Atom XML responses and zero page errors. This includes all five locales, 1440/390/320
  widths, dark mode, related links, canonical topics, subscriptions, content analytics,
  freshness advisory pagination, and the separate unpublished lab draft preview.
- Freshness checks requested `view=due&page=2` and retained the published-candidate review
  URL. Subscription clicks actually wrote/read the exact localized Atom URL via Clipboard.
- The lab draft table/code reached their horizontal ends: at 390px the scrollLeft values
  were 98/61; at 320px they were 168/131, each equal to scrollWidth minus clientWidth.
  The outer document remained within the viewport. The table's final column and code
  right edges, plus the subscription copied status, were independently visually reviewed.
- Final evidence: <home>/.codex/tmp/mokaair-news-upgrade-20261110/visual-02/visual-results.json
  and capture-02.log. visual-01 is retained; its incomplete affiliate fixture caused a
  neighboring old-report NaN, fixed only in the off-repo capture fixture before visual-02.
- The layout-review agent reported visual PASS without blocking clipping/overlap findings.
  The lab article is mock-API preview content only; no source pack or live article was added
  by this task. Root owns final task completion/commit and any subsequent approval flow.
