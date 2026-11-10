---
id: 2026-10-21-s57-r7-narrow-author-repair-after
title: S57 R7 narrow author repair after formal R6 HOLD
status: done
priority: P2
area: docs
owner: codex-s57-author
claimed_at: 2026-10-21T00:02:54Z
created_at: 2026-10-21T00:02:51Z
completed_at: 2026-10-21T00:10:53Z
branch:
depends_on:
  - 2026-10-20-s57-r6-fixed-or-narrative-merge
scope:
  - docs/videos/curio-s57/brief.md
  - docs/videos/curio-s57/claims.md
  - docs/videos/curio-s57/video.json
  - docs/videos/curio-s57/script.md
  - docs/videos/curio-s57/review/r7-author-fix.md
  - docs/videos/curio-s57/review/r7-author-diff.patch
---

# S57 R7 narrow author repair after formal R6 HOLD

## Why

R6 獨立書面畫面覆核擋 `s57150` 多人互動 prompt，兩位盲讀共同擋「仍要考察／不返家」重播；需在 R6 正式合併封存後給新一版作者窄修。

## Definition of done

- [x] R7 具可追溯逐行差分、五檔 SHA、無自我核准的作者交接；已清除已知多人 prompt 與共同重播，仍待新版本獨立審查。

## Steps

- [x] 確認 R6 固定 OR 官方 CLI、原票與五檔雜湊均已封存。
- [x] 只刪四個重複場景、改八句／claims 及六個相關 prompt，重生 script，保留 18→19→20 日順序。
- [x] 保留 45 秒開場、八分鐘以上正文、15 loops、89.0% 可愛懸疑插畫鏡頭。
- [x] 再核逐字主張對齊、lint、docs tests、任務檢查；凍結五 SHA 並向協調者交付，未做媒體。

## How to verify

`git apply --check --reverse docs/videos/curio-s57/review/r7-author-diff.patch`；`sha256sum docs/videos/curio-s57/{research.md,brief.md,claims.md,video.json,script.md}`；`node tools/video/cli.mjs lint --slug curio-s57 --json`；`npm run test:docs-videos`；`npm run check:tasks`。

## Notes

[R7 作者凍結交接](../../docs/videos/curio-s57/review/r7-author-fix.md)列全部 R6／R7 SHA、變更 ID、固定史料與限制。R7 163／163 claims/scene 逐字對齊、lint 0／0、docs 236／236 pass，正文 2,610 漢字按 325／分約 8.03 分。R6 A 單票書信岔段異議仍在，新盲讀須獨立評；R7 尚未史料／敘事／畫面 PASS，也無語音、插圖、配樂或人工核准。
