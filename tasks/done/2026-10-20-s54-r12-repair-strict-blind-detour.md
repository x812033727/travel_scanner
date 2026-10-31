---
id: 2026-10-20-s54-r12-repair-strict-blind-detour
title: S54 R12 repair strict blind detour and payment payoff
status: done
priority: P2
area: docs
owner: codex-s54-r12-author
claimed_at: 2026-10-20T21:31:30Z
created_at: 2026-10-20T21:31:27Z
completed_at: 2026-10-20T21:36:52Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s54/brief.md
  - docs/videos/curio-s54/research.md
  - docs/videos/curio-s54/claims.md
  - docs/videos/curio-s54/video.json
  - docs/videos/curio-s54/script.md
  - docs/videos/curio-s54/review/r12-author-fix.md
---

# S54 R12 repair strict blind detour and payment payoff

## Why

S54 R11 的兩位無背景盲讀者正式 OR 為 12／13，唯一共同失敗是 `no_detour`：五月郵票主問題回答後，尾端轉去 1848 年 Leavitt 的回信貼票用法。第二位讀者也指出開場付款問題回收過泛，以及郵差等收錢的資訊重述。需以同一時間線上的史料修稿後，再交給不同工作者重做來源、畫面與雙盲審查。

## Definition of done

- [x] 刪除 1848 年口播岔路，五月結尾以史料可核的防重用問題、當時處理與暫時觀察收束。
- [x] 開場付款問題有直接回收；重複付款句刪除，最快正文仍達八分鐘。
- [x] 企劃、研究、逐句主張、影片場景和劇本五份凍結檔的雜湊與作者紀錄一致；本輪未自評獨立審查。

## Steps

- [x] 依希爾 1840 年 1 月與 5 月紀錄改寫對應口播、畫面提示、主張及 loop 對應。
- [x] 更新企劃節奏、研究來源、劇本和 R12 作者凍結紀錄。
- [x] 保留 S54 TTS STOP；舊稿六句草稿快取沒有接入新版。

## How to verify

- `node tools/video/cli.mjs lint --slug curio-s54 --json`：0 errors、0 warnings。
- `sha256sum docs/videos/curio-s54/{brief.md,research.md,claims.md,video.json,script.md}`：與 `docs/videos/curio-s54/review/r12-author-fix.md` 的五筆 SHA-256 相符。
- `npm run check:tasks`：通過。作者紀錄另列劇本時長估算與待審項。

## Notes

R11 正式結果見 `docs/videos/curio-s54/review/r11-clean-merge.md`，R12 作者差分及史料行號見 `docs/videos/curio-s54/review/r12-author-fix.md`。下一步須由不同工作者審查史料和畫面，並讓兩位完全無先前對話背景的讀者重做 13 題敘事；在新稿全部通過前不得繼續 TTS。
