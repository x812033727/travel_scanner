---
id: 2026-09-28-localize-pestle-and-swot-tows-guides
title: Localize PESTLE and SWOT/TOWS guides in five languages (Batch039 Pair B)
status: in-progress
priority: P1
area: docs
owner: codex-batch039-pair-b
claimed_at: 2026-09-28T12:23:21Z
created_at: 2026-09-28T12:22:56Z
completed_at:
branch: codex/article-localization-039-strategy-b
depends_on: []
scope:
  - apps/api/app/guides/content/pestle-business-scan.json
  - apps/api/app/guides/content/swot-tows-action-plan.json
  - apps/web/public/guides/pestle-business-scan
  - apps/web/public/guides/swot-tows-action-plan
  - docs/article-localization/batch039-pair-b-evidence.md
  - tasks/open/2026-09-28-localize-pestle-and-swot-tows-guides.md
---

# Localize PESTLE and SWOT/TOWS guides in five languages (Batch039 Pair B)

## Why

Both published zh-TW strategy guides have complete 33-block source articles but no
zh-CN, English, Japanese or Korean documents. Their hero and diagram artwork has
Chinese text. Batch039 Pair B adds full reviewable translations and locale artwork
without altering the published originals.

## Definition of done

- [x] Both packs contain complete zh-CN, en, ja and ko title, description, body, table, alt, caption and source-title translations.
- [x] Each target locale has a translated hero SVG/JPG and diagram SVG with browser-checked text fit.
- [x] Pinned source facts, qualifiers, URLs/dates, exact ArticleInline targets, and zh-TW/root metadata survive structural and hash audit.
- [ ] A scoped evidence record and draft PR are ready for editorial review; live release remains a separate gate.

## Steps

- [x] Confirm #914 merged, reuse its clean worktree, branch from current main, verify freeze and task scopes, and claim this task.
- [x] Translate and review all four target documents for both articles.
- [x] Render and inspect localized SVGs and hero JPGs across all target locales.
- [x] Run scoped lint, API/web tests, task check, browser layout QA and final content/asset hash audit.
- [ ] Open draft PR only after content QA and record any external CI blocker.

## How to verify

Run `uv run python -m app.guides.pack_cli lint --kind life --slug pestle-business-scan --slug swot-tows-action-plan`, focused guide content/link/ingest API tests, targeted article/image web tests and typecheck, `npm run check:tasks`, final content/asset hash audit, and browser previews recorded in `docs/article-localization/batch039-pair-b-evidence.md`.

## Notes

- #914 is merged and the reused worktree was clean. Branch base `origin/main` was `c54594e488f48e3655566cc8a86d45e9dc2e004e` before drafting.
- Pinned candidate inventory SHA-256 `3ce92eeeb90f1793988308dacf1d93729b5a0ee61d8e0e98a9a769e68c7d666f`; guarded four-lock read-only receipt `C:/Users/x8120/.codex/article-localization-release/batch039-strategy-readonly-inventory-20260928/receipt-20260928T115126Z.json` SHA-256 `e156935e618b5233d63a5c8981db2dda0837f9cfceefded365fdd75d9485024f`. Both source packs and six original assets still match inventory on current main; receipt captured published zh-TW v4 with no target locales at 2026-09-28T11:51:28Z.
- The earlier two Alembic migration heads were joined by main PR #918. This branch will be updated to that main before the draft PR; PR CI remains an independent check.
- Final audit: 26 content/asset files, zero issues; 16 final SVG browser cases and 16 desktop/mobile article preview cases, zero issues. API guide tests: 67 passed, 5 skipped; pack lint, web typecheck, task check, and diff check pass. Local Windows Vitest stopped at thread-worker startup for all three targeted guide suites and did not execute assertions; PR CI must validate them. Details and hashes: `docs/article-localization/batch039-pair-b-evidence.md`.
