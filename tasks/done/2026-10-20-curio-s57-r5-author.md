---
id: 2026-10-20-curio-s57-r5-author
title: Repair S57 R4 narrative holds in R5 author draft
status: done
priority: P2
area: docs
owner: codex-s57-author
claimed_at: 2026-10-20T23:30:02Z
created_at: 2026-10-20T23:26:43Z
completed_at: 2026-10-20T23:32:33Z
branch:
depends_on:
  - 2026-10-20-s57-r4-formal-narrative-merge-and
scope:
  - docs/videos/curio-s57/brief.md
  - docs/videos/curio-s57/claims.md
  - docs/videos/curio-s57/video.json
  - docs/videos/curio-s57/script.md
  - docs/videos/curio-s57/review/r5-author-fix.md
  - docs/videos/curio-s57/review/r5-author-diff.patch
---

# Repair S57 R4 narrative holds in R5 author draft

## Why

S57 R4 雖通過獨立史料與書面畫面查核，正式雙盲敘事合併僅 9／13；兩位新讀者共同指出章節銜接、提問回收、重述及東行岔題。需在不破壞來源層級及 2 月 18→19→20 日時序下窄修，另凍結交審。

## Definition of done

- [x] R5 作者候選按四個正式未過題窄修，正文至少 8 分鐘、來源逐句可查、五份創作檔與差異 SHA 凍結，交由獨立審閱。

## Steps

- [x] 依 R4 正式票及固定兩原文修 `video.json`、`claims.md`、`brief.md`，重生 `script.md`；研究版本不變。
- [x] 凍結五檔、記錄逐行 patch、完成 lint、docs tests、主張對齊及交接；不自評來源或敘事 PASS。

## How to verify

`sha256sum docs/videos/curio-s57/{research.md,brief.md,claims.md,video.json,script.md}` 對照 `review/r5-author-fix.md`；`node tools/video/cli.mjs lint --slug curio-s57 --json`（0 errors／0 warnings）；`npm run test:docs-videos`（236 pass／0 fail）；`npm run check:tasks`（exit 0）；檢查 claims 171／171 逐字對齊。

## Notes

作者交接：`docs/videos/curio-s57/review/r5-author-fix.md`；精確差異：`docs/videos/curio-s57/review/r5-author-diff.patch`。R5 僅為作者候選，R4 來源 PASS 不外推；獨立來源、兩位新嚴格盲讀及正式合併須綁定 R5 新 SHA。未執行付費媒體。
