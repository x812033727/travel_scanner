---
id: 2026-09-28-localize-newsletter-content-guides-batch035-pair
title: Localize Kit and content marketing guides (batch 035 pair B)
status: done
priority: P1
area: docs
owner: codex-p1-audit
claimed_at: 2026-09-29T02:12:17Z
created_at: 2026-09-28T07:45:58Z
completed_at: 2026-09-29T02:12:23Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - apps/api/app/guides/content/kit-newsletter-setup.json
  - apps/api/app/guides/content/content-marketing-calendar.json
  - apps/web/public/guides/kit-newsletter-setup
  - apps/web/public/guides/content-marketing-calendar
  - docs/article-localization/batch035-pair-b-evidence.md
  - tasks/open/2026-09-28-localize-newsletter-content-guides-batch035-pair.md
---

# Localize Kit and content marketing guides (batch 035 pair B)

## Why

The published Kit newsletter and content-marketing-calendar articles have only
zh-TW locale rows (article v2, zh-TW published v4 at the 2026-09-28 inventory).
This pair contributes eight missing locale documents and 24 localized image
assets to Batch035. See the SHA-pinned read-only inventory under
`C:\Users\x8120\.codex\article-localization-release\batch035-newsletter-readonly-inventory-20260928\inventory.json`.

## Definition of done

- [x] Both source zh-TW documents and root metadata stay unchanged.
- [x] Complete zh-CN/en/ja/ko documents preserve all 33 blocks, tables,
      warnings, checked dates and source URLs, with translated title, description,
      alt text, captions and source titles.
- [x] Eight localized hero SVGs, eight raster hero JPGs and eight diagram SVGs
      pass layout and visual review.
- [x] Unpublished target-locale article destinations remain non-clickable.
- [x] Scoped pack lint and repository task checks pass; open a reviewable PR.

## Steps

- [x] Verify remote main and both source pack hashes against live inventory.
- [x] Claim exact pair scope in an isolated worktree.
- [x] Translate and review eight locale documents.
- [x] Render and inspect 24 localized assets.
- [x] Validate, commit, push and open the pair PR.

## How to verify

`uv run python -m app.guides.pack_cli lint --slug kit-newsletter-setup` and
`uv run python -m app.guides.pack_cli lint --slug content-marketing-calendar`
from `apps/api`; `npm run check:tasks` from repo root; inspect SVG and raster
previews at 1600×900 plus layout receipts.

## Notes

Base `origin/main=e36db07bbb1a511046def7c42cd6978f3888cc52`.
Source SHA-256: Kit `8bfc7cf36262d67b36e35bcaa7a8378e835833ac7fd000ca98c32f8e10679677`;
calendar `30beb6bb2b3819a560e037d8a28f14b6ae42d18094001ef5a3b2f5004a261a18`.
The source inline links point at locales that were unpublished in the pinned
inventory. Target drafts retain ArticleInline slug/kind and translated labels.
The API resolves only same-locale published targets, and the web component
renders unresolved references as plain text.
Independent editorial reviews of both articles have passed after diagram-copy
corrections. Receipts and canonical hashes are in the scoped evidence document.
Draft PR: https://github.com/x812033727/travel_scanner/pull/900 .
The content is not deployed, imported or published; live browser/device QA is pending.


## 2026-09-29 標記完成（由站主授權，非原持有者）

站主要求逐張核對原 64 張 P1 並處理已無剩餘工作的票，並明確確認本次 30 張封存、2 張刪除。本次只結案，不重做已合併實作。
原持有者：codex-root；原分支：codex/article-localization-035-newsletter-b。

- PR #900 merged 2026-09-28; both main packs have five locales and scoped evidence record exists.
- DoD is reviewed complete drafts/24 assets and open reviewable PR; publication explicitly separate.

上述後續證據補足舊清單仍未勾選的項目，已同步勾選。歷史限制保留供追溯；這是既有完成紀錄的核對，不宣稱本日重新部署、重新發布或重新跑過歷史測試。

Live release remains separate and is not claimed.

`--force` 僅用於本次授權的任務結案記帳，未修改或接管原分支實作；已核對 main 與開啟 PR，完成判定依上列證據。Windows 的 tasks done 搬移曾留下 open 副本，本次用 Git 原子搬移保留完整任務紀錄。
