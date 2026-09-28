---
id: 2026-09-28-batch040-pair-b-ecommerce-zero-click
title: Localize ecommerce product SEO and zero-click guides in five languages (Batch040 B)
status: in-progress
priority: P1
area: docs
owner: codex-batch040-pair-b
claimed_at: 2026-09-28T13:38:35Z
created_at: 2026-09-28T13:37:49Z
completed_at:
branch: codex/article-localization-040-seo-b
depends_on: []
scope:
  - apps/web/public/guides/ecommerce-product-seo
  - apps/web/public/guides/zero-click-search-strategy
  - docs/article-localization/batch040-pair-b-evidence.md
  - tasks/open/2026-09-28-batch040-pair-b-ecommerce-zero-click.md
---

# Localize ecommerce product SEO and zero-click guides in five languages (Batch040 B)

## Why

The published zh-TW ecommerce product SEO and zero-click search guides have no
zh-CN, English, Japanese, or Korean content. Their original hero and diagram
artwork carries Chinese text. Batch040 B adds complete reviewable translations
from the corrected #930 source revision without changing live production.

## Definition of done

- [ ] Both 33-block packs have complete zh-CN, en, ja, and ko documents,
      including title, description, body, tables, captions, alt text, and sources.
- [ ] Each target locale has a translated hero SVG/JPG and diagram SVG with
      browser-checked text fit.
- [ ] Source qualifications, URLs/check dates, remaining ArticleInline targets,
      original zh-TW/root metadata, and artwork pass scoped integrity audit.
- [ ] A draft PR and evidence record are ready for review; live import and
      publication remain separately gated.

## Steps

- [x] Verify #930 correction head and create an isolated worktree and task.
- [x] Freeze corrected repository source and original artwork hashes; compare
      the read-only production receipt without claiming that the correction is live.
- [x] Translate all eight target documents outside the repository while #930
      still owns both JSON file scopes.
- [x] Render and inspect localized artwork across all four target locales.
- [ ] After #930 merges and its task releases the JSON paths, add those exact
      pack paths to this scope and install the translated documents.
- [ ] Run pack lint, focused API/Web checks, browser layout, task check and
      content/asset hash audit, then open a draft PR.

## How to verify

Use scoped `pack_cli lint`, focused guide content/link/ingest API tests,
targeted article/image Web tests and typecheck, `npm run check:tasks`, and
final content/asset and browser-layout reports in
`docs/article-localization/batch040-pair-b-evidence.md`.

## Notes

- Branch `codex/article-localization-040-seo-b` starts at #930 corrected head
  `128c3f3cd877da4aec1e1c5ad3a4cb8310449793`. Its source-fix task is in
  review and owns both JSON paths, so this task initially claims only the image
  directories, evidence, and its own task file. No force claim or concurrent
  JSON edits; scope expansion follows #930 merge/task release.
- Root shared the guarded four-lock read-only production receipt
  `C:/Users/x8120/.codex/article-localization-release/batch040-commerce-search-readonly-inventory-20260928/receipt-20260928T133638Z.json`, SHA-256
  `676b67043693c188020e6adf9d5b16bd1e25a4b0a44f8660ed6034fb970dcd0d`.
  It records active/published article v2, zh-TW draft/published v4 matching
  pre-correction main, and no target-locale rows. The corrected #930 source is
  not yet live; a later release needs explicit reconciliation/preflight.
- Final staged Chromium artwork layout: 16/16, zero issues, SHA-256
  `b1942ede56c4d84e50eb4f5e8af315eb363406656b793df2ab3cff9b9c2fde15`;
  independent visual review passed. Staged desktop/mobile article preview:
  16/16, zero issues, SHA-256
  `0c5cbf1263ec17a9cc337d89dda8785cf93ec58f646810636d34faa163cd7cd4`.
- Corrected repository source pack hashes remain
  `0a4898673b9587fcc1acf6f2edeaf0eab09e677f48b34325536948fb6260a75d`
  and `a6d3adc5d49c9afe1520a3ac72d353e862f8831c588c7a520af21f20ee6f09db`;
  current production still has the pre-correction source as of the pinned
  read-only receipt.
