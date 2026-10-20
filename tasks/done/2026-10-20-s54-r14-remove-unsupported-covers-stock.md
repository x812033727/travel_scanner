---
id: 2026-10-20-s54-r14-remove-unsupported-covers-stock
title: S54 R14 remove unsupported covers stock attribution
status: done
priority: P2
area: docs
owner: codex-s54-r14-author
claimed_at: 2026-10-20T21:50:46Z
created_at: 2026-10-20T21:50:43Z
completed_at: 2026-10-20T21:51:39Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s54/brief.md
  - docs/videos/curio-s54/claims.md
  - docs/videos/curio-s54/video.json
  - docs/videos/curio-s54/script.md
  - docs/videos/curio-s54/review/r14-author-fix.md
---

# S54 R14 remove unsupported covers stock attribution

## Why

R13 的獨立史料覆核只對 `s54135` 的備貨者主語提出 HOLD。希爾固定原文只說大量封套已備妥，未說是希爾本人備貨；新版需要保留需求轉向附膠郵票的意思，刪除無據主語並重凍結。

## Definition of done

- [x] `s54135` 不再把封套備貨歸於希爾，主張表與劇本口播完全對齊。
- [x] 五份凍結檔 SHA 記錄完整，劇本維持最快正文超過八分鐘，影片 lint 0 錯誤／0 警告。
- [x] S54 STOP 留在原位；交其他工作者定點史料覆核與無背景雙盲審查。

## Steps

- [x] 改 `video.json` 與 `claims.md` 的 `s54135`，重新產生 `script.md`。
- [x] 修正 `brief.md` 的字數及書面時長，撰寫 `review/r14-author-fix.md`。

## How to verify

- `node tools/video/cli.mjs script --slug curio-s54`：重新產生劇本。
- `node tools/video/cli.mjs lint --slug curio-s54 --json`：0 errors／0 warnings。
- `sha256sum docs/videos/curio-s54/{brief.md,research.md,claims.md,video.json,script.md}`：與 R14 作者紀錄一致。
- 場景、主張、劇本 145／145 逐字對齊；`npm run check:tasks`、`git diff --check` 通過。

## Notes

固定史料 H 13390–13399 對備貨者沒有主語；本輪不改其餘敘事與畫面。R14 作者差分與待審關卡見 `docs/videos/curio-s54/review/r14-author-fix.md`。未做 TTS 或自評獨立史料與敘事。
