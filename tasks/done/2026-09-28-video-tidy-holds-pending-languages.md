---
id: 2026-09-28-video-tidy-holds-pending-languages
title: 清工作檔前等待審的語言批次
status: done
priority: P2
area: tools
owner: codex-video-tidy
claimed_at: 2026-09-29T09:50:15Z
created_at: 2026-09-28T15:33:39Z
completed_at: 2026-09-29T10:01:26Z
branch: codex/video-tidy-pending-reviews
depends_on: []
scope:
  - tools/video/automation/tidy.mjs
  - tools/video/automation/tidy.test.mjs
---

# 清工作檔前等待審的語言批次

## Why

#921（`f0a832941`）讓工人在影片上 YouTube 滿 7 天後清掉工作檔，`tidy.mjs:47` 的第一個目標就是成片 `final.mp4`。清之前的語言檢查（`tidy.mjs:233-239`）只在某個語言部件是 `working` 時才等，但一批還在等站主審的語言批次，部件已經顯示 `ready`：`apps/api/app/video_reviews/admin_service.py:152-193` 的 `language_states` 讀的是 status 為 pending 或 approved 的批次。

帶配音的語言批次一定停在 pending 等站主（`languages_need_owner`，同檔 :197-206），而配音只能加在已上 YouTube 的影片上，所以這種批次常常拖過發布後第 7 天。這時工作檔被清掉，站主再把那批退回（`decide()` :770-786，審查卡每個 pending 關卡都有退回鈕），部件回到 `working`，工人的 `Automation.languages()` 卻因為 `final.mp4` 不在（`tools/video/core/approvals.mjs:74` 回 `absent`，`tools/video/automation/flow.mjs:1535` 直接 return null）每一輪都什麼也不做。`/admin/videos` 那一格永遠停在「製作中」，沒有任何說明。

站主貼了網址、沒填發布時間、發布核准又已經超過 7 天時，影片在下一輪就到期，即使配音批次還在 pending，所以這不是理論上的情況。`2026-09-28-video-tidied-late-languages` 只處理「清完之後才勾新語言」，重做不了被退回的批次。

2026-09-28 部署 `50b3cb55` 後的稽核找到的（兩個代理獨立確認）。

## Definition of done

- [x] 影片還有任何語言批次在等站主審（站上的 `ProjectSummary.pending > 0`，`apps/api/app/video_reviews/schemas.py:195`，或任何 pending 的 languages review）時，清理不動它，並在那一輪的 tidy 行寫出「等語言批次審完」。
- [x] 沒有待審批次的影片照舊在第 7 天清。

## Steps

- [x] 在 `tidy.mjs` 的語言判斷裡加上待審批次的條件（site 讀不到時維持現在的保守行為：不清）。
- [x] `tidy.test.mjs` 加兩個案例：批次 pending → 不清；批次核准 → 清。現在只測了 `working`（:242-258）。

## How to verify

```bash
node --test "tools/video/automation/*.test.mjs"
npm run test:tools
```

## Notes

2026-09-29：以 main `716bd5dc` 重新確認問題，11 張開啟中 PR、43 個非 main
遠端分支與 218 個已登記 worktree 都沒有這兩檔的活躍競爭修改（42 個舊路徑
已不存在，兩個舊 sparse checkout 無這兩檔）。認領使用 `--force` 僅略過三張
舊廣 scope 票：dubs-worker、drama-room-worker、split-settings-worker 的程式
已隨 #870（`79e26fcd`）合併。它們原有的驗收待辦與認領紀錄保持不動。

稽核的原始推論與行號在 PR 說明裡。修法的另一個方向是清理時保留 `final.mp4`，但那會讓清理省下的空間大減，先不採用。

### 2026-09-29 實作與驗證

- 在判定到期／刪檔之前，以 `ProjectSummary.pending > 0` 保留已上 YouTube
  的影片。API 此欄計算所有待審 gate，故其他待審工作也保守保留；不把
  ready／uploaded 的語言部件誤當成整批已核准。
- 自動 worker 平常的 `roundLines()` 原本隱藏所有 held 原因，已補上待審
  這一類的訊息。其他等待狀態維持原本安靜行為，verbose 不會重複同一支。
- 六個新案例使用真正的臨時媒體檔：pending 1／2 × 正常／dry-run、核准後
  pending=0 可清、退回後 pending=0 但部件 working 仍保留；同時核對媒體
  bytes、`auto.json` 未被改寫，以及兩種日誌模式。
- 原碼回歸為 22 passed／5 failed／1 skipped，五個失敗皆重現待審仍被清理。
  最終 focused 為 27 passed／1 Windows 檔案 symlink 權限 skip，automation
  為 120 passed／1 skip；完整 tools 為 725 passed／2 skipped，exit 0。
  Windows 使用 bundled Node 24.21 與 `--test-concurrency=1`，未排除任何檔案。
- 獨立實作／資料保護／日誌檢查通過；開 PR 前再次確認沒有新 scope 碰撞。
  只操作可拋棄的本機測試檔，未讀取或清理正式站任何影片或資料。
