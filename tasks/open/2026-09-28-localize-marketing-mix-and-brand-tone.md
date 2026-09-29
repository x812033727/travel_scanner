---
id: 2026-09-28-localize-marketing-mix-and-brand-tone
title: Localize marketing mix and brand tone guides in Batch 036 Pair B
status: review
priority: P1
area: docs
owner: codex-root
claimed_at: 2026-09-28T10:00:53Z
created_at: 2026-09-28T09:20:03Z
completed_at:
branch: codex/article-localization-036-marketing-b
depends_on: []
scope:
  - apps/api/app/guides/content/marketing-mix-models.json
  - apps/api/app/guides/content/brand-tone-vibe-marketing.json
  - apps/web/public/guides/marketing-mix-models
  - apps/web/public/guides/brand-tone-vibe-marketing
  - docs/article-localization/batch036-marketing-pair-b-evidence.md
---

# Localize marketing mix and brand tone guides in Batch 036 Pair B

## Why

Both published life guides still have only their zh-TW source revision. The
2026-09-28 read-only inventory pinned published article v2 / zh-TW v4 and
confirmed four missing locale rows per article. Add complete target-language
drafts and translated original Mokaair illustrations before any import.

## Definition of done

- [x] Add complete zh-CN/en/ja/ko documents for both articles with 33 blocks,
      translated titles, descriptions, tables, source titles, alt text and captions.
- [x] Preserve article metadata, published zh-TW prose, source URLs/dates and
      all three original ArticleInline targets per locale.
- [x] Add and render 24 localized image assets without overflow or overlap.
- [x] Obtain independent editorial review of meaning, figures and navigation.
- [ ] Obtain green PR checks before merge.
- [ ] Import/publish guarded locale revisions and verify live pages separately.

## Steps

- [x] Confirm inventory and source versions, claim narrow pair scope.
- [x] Complete eight language documents and 24 image assets.
- [x] Run content/asset and render audits, focused tests and task checks.
- [x] Open draft PR and record its URL and CI status.

## How to verify

From `apps/api`, run pack lint for `marketing-mix-models` and
`brand-tone-vibe-marketing`, then `uv run pytest tests/test_guides_content_pack.py
tests/test_guides_content_links.py -q`. From the root, run `npm run test
--workspace @travel-scanner/web -- components/content-blocks.test.tsx` and
`npm run check:tasks`. The scoped evidence document pins source, document,
asset, render and audit SHA-256 values.

## Notes

The original subagent exhausted its usage limit after drafting the packs and
assets; codex-root released and reclaimed this task to finish validation. The
English brand description was shortened from 520 to 498 characters to satisfy
the schema. Two target ArticleInline nodes per locale were restored so that
the runtime resolver can activate same-language links when destinations are
published; until then it renders plain text. The English brand diagram heading
font was reduced from 35 to 33 after browser measurement found card overflow.
Both packs lint with only existing `no_summary` and advisory English length
warnings. Focused API tests: 12 passed, 5 skipped; web: 65 passed. All 16 SVGs
passed canvas/card/overlap measurement and eight raster heroes are 1600x900.
Independent read-only editorial review marked both articles GO. Unpublished
same-locale related-reading targets intentionally remain plain text. Live
browser QA is still pending.
Draft PR: https://github.com/x812033727/travel_scanner/pull/907.
CI began on the submitted branch; merge remains gated on independent editorial
review and green checks.

### 2026-09-29 看板盤點與站主決定

站主已同意「準備逐批發布清單與步驟，再讓我確認」。本輪一次正式站唯讀盤點已完成；發布清單、精確來源雜湊、依賴與逐步驗收見 docs/work-status-2026-09-29-article-release-plan.md。未授權正式寫入、部署或發布；原門檻維持。

本次僅追加交接證據，不改既有owner、scope、branch或執行狀態。
