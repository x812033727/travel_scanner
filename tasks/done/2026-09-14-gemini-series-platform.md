---
id: 2026-09-14-gemini-series-platform
title: Gemini series content blocks and navigation
status: done
priority: P2
area: web
owner: codex-gemini-series
claimed_at: 2026-09-14T05:57:47Z
created_at: 2026-09-14T05:57:44Z
completed_at: 2026-09-14T08:57:57Z
branch:
depends_on: []
scope:
  - apps/api/app/guides/schemas.py
  - apps/api/app/guides/admin_service.py
  - apps/api/app/guides/pack_ingest.py
  - apps/api/tests/test_gemini_series.py
  - apps/api/tests/test_guide_rich_blocks.py
  - apps/web/lib/content-blocks.ts
  - apps/web/lib/content-blocks.test.ts
  - apps/web/lib/guides.ts
  - apps/web/lib/guides.test.ts
  - apps/web/lib/gemini-series.ts
  - apps/web/components/guides/gemini-series-navigation.tsx
  - apps/web/components/guide-code-block.tsx
  - apps/web/components/guide-rich-editor.tsx
  - apps/web/lib/guide-series-copy.ts
  - apps/web/lib/guide-series.ts
  - apps/web/lib/guide-series.test.ts
  - apps/web/lib/guide-series.json
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
  - apps/web/components/guides/code-block.tsx
  - apps/web/components/guides/series-index.tsx
  - apps/web/components/guides/series-navigation.tsx
  - apps/web/components/guides/series.test.tsx
  - apps/web/components/guides/article.tsx
  - apps/web/components/guides/article-page.tsx
  - apps/web/components/admin-guides-panel.tsx
  - apps/web/components/admin-guides-panel.test.tsx
  - apps/web/app/[locale]/life/page.tsx
  - apps/web/messages/en/common.json
  - apps/web/messages/en/admin.json
  - apps/web/messages/zh-TW/common.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/ko/admin.json
  - apps/web/e2e/gemini-series.spec.ts
  - tools/gemini-series.mjs
  - tools/gemini-series.test.mjs
  - docs/gemini-series
  - docs/life-ai-series.md
  - docs/life-ai-series-brief.md
  - docs/travel-guides.md
---

# Gemini series content blocks and navigation

## Why

The approved 50-lesson Gemini series needs one searchable server-rendered directory, shared navigation, inline article links, and copyable examples in the existing structured article system. Old articles must remain readable and the hub must only become visible after every child is ready.

## Definition of done

- [x] All 50 articles can be found through the hub, routes, keywords and command links on desktop/mobile and without JavaScript.
- [x] Rich paragraphs and literal code survive validation, editor save/reopen, preview, import and public rendering.
- [x] Scoped release stops on a partial failure and publishes the hub only after all children are verified.

## Steps

- [x] Add backend/frontend rich paragraph and code schemas, rendering and editing.
- [x] Add the authoritative catalogue, learning paths, search and series navigation.
- [x] Add dry-run-first release orchestration and partial-failure tests.
- [x] Verify editor save/reopen with new blocks and browser/mobile/no-JavaScript flows.
- [x] Finish source/asset/content validation tools and documentation.
- [x] Run required checks and verify the released public pages and sitemap.

## How to verify

Run focused web suites, `npm run typecheck:web`, `npm run check:i18n`, relevant lint and tool/task checks; run API guide tests and rich block tests. Run `node tools/gemini-series.mjs check` after all 51 content packs and images exist. Browser verification must include MD, GEMINI.md, 手機, CLI, /memory and NotebookLM searches; article back/previous/next links; copy; mobile overflow; and the public release gate.

## Notes

2026-09-14: Focused web suites passed 80 tests; typecheck and all five locale checks passed. API guide/rich-block suites passed 77 tests, with 67 environment-dependent tests skipped. Seven release-tool tests passed. These results do not establish production publication or real Gemini account testing. The catalogue and hub publication status control visibility without adding a database table. No deployment or publication has occurred.

2026-09-14: Complete local suite passed: 115 related web tests, 18 API tests (8 PostgreSQL skips), 8 Playwright tests on production-mode Next with all 51 real packs, build, web lint/typecheck, API mypy (327 files), and i18n/task checks. The latest main now includes a separate Claude Code series with shared rich/code schemas and navigation; reconcile this before final acceptance and release.

2026-09-14 integration acceptance: reconciled with main f5b814cb and preserved Claude Code shared blocks/series. The 51 complete packs and 102 reviewed illustrations pass catalogue, length, assets and links; 109 snippets and four deterministic executions pass. Final production-build Playwright: 8 passed (all 50 lessons on desktop/mobile, no-JavaScript 360px, copy, anchors, six searches, unpublished-hub gate). API: 32 passed / 16 PostgreSQL-dependent skipped locally; web integration: 68 passed plus final 34 UI tests; tools: 48 passed. Build, lint, typecheck, i18n, Ruff and mypy pass. CI and production publication are still pending. Existing twenty batch-05 slugs are reused; the comparison is labeled official-feature comparison and reproducible test procedure, without fabricated benchmark results.

2026-09-14 completed: PR #490 merged as 4ba38e81cd48e2c3f8920b9dee1108b5cdba50d6; post-merge CI 34822723832 passed. Verified backup, deployed eight application services, preserved PostgreSQL/Redis containers and selected stable fingerprints. All 51 zh-TW pages are published at https://mokaair.com/zh-TW/life/gemini-guide . Hub read verification failed after its write; the stopped run was reconciled by exact read-only comparison of all 51 documents without another import. Public Chromium verification passed all 50 lessons on desktop and mobile (100 views), 12 search checks, eight groups, five routes, copy, anchors and 360px no-JavaScript. All 102 public images match reviewed bytes, all 51 sitemap URLs exist once, and all 127 source URLs respond successfully. Receipts and screenshots are under docs/gemini-series/. Paid Google API calls and live three-assistant benchmarking were not performed or claimed.
