---
id: 2026-10-20-curio-s57-r4-author
title: Repair S57 R3 source chronology and narrative holds
status: done
priority: P2
area: docs
owner: codex-s57-author
claimed_at: 2026-10-20T23:17:49Z
created_at: 2026-10-20T23:17:35Z
completed_at: 2026-10-20T23:22:13Z
branch:
depends_on:
  - 2026-10-20-s57-r3-formal-narrative-merge-diagnostic
scope:
  - docs/videos/curio-s57/video.json
  - docs/videos/curio-s57/claims.md
  - docs/videos/curio-s57/script.md
  - docs/videos/curio-s57/brief.md
  - docs/videos/curio-s57/review/r4-author-fix.md
  - docs/videos/curio-s57/review/r4-author-diff.patch
---

# Repair S57 R3 source chronology and narrative holds

## Why

S57 R3 獨立史料覆核因 1872 年 2 月 18、19、20 日補給事件倒序 HOLD；正式雙盲合併 10／13 HOLD，共同未過章節銜接、問句回收及免重複三題。R4 須窄修後另凍結，交由獨立審閱。

## Definition of done

- [x] 修正補給時序、章節銜接、無法回答的提問與重複段落；維持來源分層與至少 8 分鐘正文，完成五檔 SHA 凍結及作者差異紀錄。

## Steps

- [x] 按 R3 固定來源及兩份盲讀理由，窄修 `brief.md`、`video.json`、`claims.md` 並重生 `script.md`，不改 `research.md`。
- [x] 記錄精確 R3→R4 差異、五檔 SHA、驗證結果與待審關卡，交接獨立來源及兩位新讀者。

## How to verify

`sha256sum docs/videos/curio-s57/{research.md,brief.md,claims.md,video.json,script.md}` 對照 `review/r4-author-fix.md`；`node tools/video/cli.mjs lint --slug curio-s57 --json`（0 errors／0 warnings，183 景）；`npm run test:docs-videos`（236 pass／0 fail）；`npm run check:tasks`（exit 0）。

## Notes

作者交接：[R4 修訂及 SHA](../../docs/videos/curio-s57/review/r4-author-fix.md)；[逐行差異](../../docs/videos/curio-s57/review/r4-author-diff.patch)。R4 只是作者候選稿；來源／畫面、兩位新盲讀與正式合併須依新 SHA 重審。未執行付費媒體，也未自評 PASS。
