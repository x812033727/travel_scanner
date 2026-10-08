---
id: 2026-09-28-localize-marketing-mix-and-brand-tone
title: Localize marketing mix and brand tone guides in Batch 036 Pair B
status: done
priority: P1
area: docs
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T04:54:42Z
created_at: 2026-09-28T09:20:03Z
completed_at: 2026-10-07T06:11:00Z
branch: codex/article-missing-locales-20261007
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
- [x] Obtain green PR checks before merge (original content PR #907 landed).
- [x] Hand off guarded publication/live verification to a separate release ticket.

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
- 2026-10-04 board sweep (claude-opus-5-5-incomplete-tickets, approved by the owner): the claim by codex-root (since 2026-09-28T10:00:53Z) was stale and is released so it stops locking its scope. Landed: #907. Still open: Green PR checks before merge (done implicitly by merge); Import/publish guarded locale revisions and verify live pages.

### 2026-10-07 current completion review

The owner's new all-missing-languages request resumes this pair. Fresh production
state still lacks all eight target locale rows. Both published zh-TW hashes and
all thirty original/localized assets exactly match the old reviewed T1 package.
A current independent reviewer read every translated block and inspected fresh
SVG and actual raster contact sheets, then requested ten exact text changes:
eight published related-reading labels now equal their actual target titles,
and two zh-CN wording/script corrections use 接着 and 屏幕. Root applied only
those changes; a second read of the resulting tree passed all eight targets.

Current compiler review SHA-256:
`47a93efa3792e93cf9965a3c5cd69f7b51c4800e83595d8013669f3a06e6ec48`.
Independent final evidence SHA-256:
`15f40e62151ba5692e66930fab33b3646a5d2f46f50c179e5b0b22e2e4c3530f`.
Source hashes remain `cf9325d203eae0940db98bf6cdc8efcf691667b405a9f396e6e4f16bce937725`
and `1e43ef74156c751df615cf65d3da529fd50b5dae4ee83486e7f697e68116f728`.
New correction PR, same-image Route B rehearsal, guarded publication and live
desktop/mobile verification remain separate, unfinished stages.

### Final within-cohort review, 2026-10-07

The final release cohort also includes marketing-plan-small-business. A distinct
root executor changed the four terminal labels in marketing-mix-models to that
article's actual reviewed target titles; nothing else changed. Current mix pack
SHA is 0624bd57bf861f86dccb29a6ae6872332700e3e8f2aef57669faacdb1353d8df.
Brand remains 3f6791f71e70c97693d04fb6742e71a6c168d3d92fec4ed2ef4f7c90cb31f9dc.
Final independent T1 review SHA is
6398f3cf8d78e8a4804103447c3313ce5c599ef23d1afd8b2a86405b04e165ef.
Use the versioned life-cohort-final-review-v2 evidence, not superseded receipts.
The 13-case isolated same-image rehearsal is complete; the final expanded wave
still needs merged/deployed Git freeze and a fresh post-deployment baseline.
Publication/live verification are owned by
2026-10-07-release-localized-travel-life-wave-20261007, still open.

### Content PR handoff

PR: https://github.com/x812033727/travel_scanner/pull/1365.
Authoring, exact independent review, local validation and local installation/replay
are complete for this ticket's selected scope. Required GitHub checks and merge
remain enforced PR gates; marking this authoring ticket done does not claim those
checks are green. The PR remains draft pending owner approval.
Production deployment, publication and public desktop/mobile verification remain
open in 2026-10-07-release-localized-travel-life-wave-20261007.
Any unchecked CI/merge/publication lines above are handed to those explicit gates,
not waived or reported as completed.
