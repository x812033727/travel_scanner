---
id: 2026-10-20-curio-s57-r6-author
title: Repair S57 R5 remaining narrative recap hold
status: done
priority: P2
area: docs
owner: codex-s57-author
claimed_at: 2026-10-20T23:38:00Z
created_at: 2026-10-20T23:37:17Z
completed_at: 2026-10-20T23:41:12Z
branch:
depends_on:
  - 2026-10-20-s57-r5-formal-two-reader-narrative
scope:
  - docs/videos/curio-s57/brief.md
  - docs/videos/curio-s57/claims.md
  - docs/videos/curio-s57/video.json
  - docs/videos/curio-s57/script.md
  - docs/videos/curio-s57/review/r6-author-fix.md
  - docs/videos/curio-s57/review/r6-author-diff.patch
---

# Repair S57 R5 remaining narrative recap hold

## Why

S57 R5 固定版獨立來源 PASS，但正式雙盲合併 12／13 HOLD，兩位讀者共同判 `no_recap` 未過：勸歸先後、北岸與缺貨、所需人手及結尾分路有重述。R6 須保留歷史先後、證據層級及至少八分鐘正文，精準移除重複。

## Definition of done

- [x] 依正式診斷修共同 `no_recap`，兼收窄兩個單票異議；五份創作檔與差異雜湊凍結，供新版本獨立審閱。

## Steps

- [x] 依固定原文窄修 `video.json`、`claims.md`、`brief.md` 並重生 `script.md`；`research.md` 不變。
- [x] 記錄精確刪／改景 ID 與來源、五檔 SHA、檢查和待審關卡，不自行判定 PASS。

## How to verify

`sha256sum docs/videos/curio-s57/{research.md,brief.md,claims.md,video.json,script.md}` 對照 `review/r6-author-fix.md`；`node tools/video/cli.mjs lint --slug curio-s57 --json`（0 errors／0 warnings）；`npm run test:docs-videos`（236 pass／0 fail）；`npm run check:tasks`（exit 0）；檢查 claims 與口播 167／167 對齊。

## Notes

作者交接：`docs/videos/curio-s57/review/r6-author-fix.md`；逐行 patch：`docs/videos/curio-s57/review/r6-author-diff.patch`。R6 是作者候選，R5 的來源 PASS 不外推；新 SHA 須重作獨立來源、兩位新盲讀及正式合併。未執行付費媒體。
