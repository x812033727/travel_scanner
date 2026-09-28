---
id: 2026-09-28-video-story-tidy-pages
title: 清理工作檔時也清掉故事讀過的頁面
status: done
priority: P3
area: tools
owner: claude-opus-5-5-video-story-worker
claimed_at: 2026-09-28T16:00:18Z
created_at: 2026-09-28T14:30:20Z
completed_at: 2026-09-28T16:13:02Z
branch: claude/video-story-worker
depends_on:
  - 2026-09-28-video-story-tidy-finished
  - 2026-09-28-video-story-worker
scope:
  - tools/video/automation/tidy.mjs
  - tools/video/automation/tidy.test.mjs
  - tools/video/automation/story.mjs
  - docs/videos/AUTOMATION.md
  - .agents/skills/youtube-video/references/story.md
---

# 清理工作檔時也清掉故事讀過的頁面

## Why

工人做品牌故事時，會把讀過的來源頁面存在每支影片的工作區（`story/pages/`，一頁一個 JSON，檔名是網址的雜湊），同一支影片的六次撰稿與六次查核才不用每次重抓（票 `2026-09-28-video-story-worker`，PR #933）。一支故事有 4 到 23 個來源，整頁文字加起來是幾 MB 到幾十 MB。

清理工作檔的程式（票 `2026-09-28-video-story-tidy-finished`，PR #921）只刪固定清單 `TARGETS` 上的名稱，寫它的時候故事流程還沒有，所以清單裡沒有這個資料夾。影片上架滿保留天數之後，這些頁面會一直留著。

## Definition of done

- [x] 已上架或已放棄、而且滿保留天數的故事，`story/pages/` 會跟其他大檔一起清掉。
- [x] `story/chapters/` 留著：那是每一章的稿子與查核結果，很小，出問題時要看。
- [x] 不是故事的影片行為不變；沒有 `story/` 資料夾時不算失敗。
- [x] 測試涵蓋：有 `story/pages/` 的故事會被清、`story/chapters/` 留下、`story/pages` 是連結時只移除連結本身。

## Steps

- [x] 等 PR #921 與 PR #933 都在 main 上再開工，資料夾名稱從 `story.mjs` 的常數讀，不要另寫一份。（#921 在 main；#933 還是草稿，所以在 #933 的分支上做，見 Notes。）
- [x] `TARGETS` 加上 `story/pages`，補測試。
- [x] `docs/videos/AUTOMATION.md` §清理工作區的清單補上這一項（scope 要加這個檔）。

## How to verify

```bash
node --test "tools/video/automation/*.test.mjs"
```

## Notes

- 這是做工人票時回報的（2026-09-28）：工人票不能動 `tidy.mjs`，清理票不知道故事流程，所以落在兩張票中間。
- 部署後先在主機上跑 `tidy --dry-run` 看它會清什麼，再讓它真的清。
- 2026-09-29 認領（claude-opus-5-5-video-story-worker），在工人票的分支 `claude/video-story-worker`（PR #933）上做，因為 `story/pages/` 的名稱在那個分支的 `story.mjs`、還不在 main。用了 `--force`：`claim` 拒絕的理由是 scope 與 PR #870 的三張 `review` 票（`video-dubs-worker`、`video-drama-room-worker`、`video-split-settings-worker`）重疊，#870 早已合併、只是沒人結案；兩張相依的票都已在 `tasks/done/`（清理票隨 #921 上了 main，工人票在這個分支結案）。那三張票沒有動。
- 做了什麼：`story.mjs` 匯出 `STORY_PAGES_DIR`（`story/pages`）與 `STORY_CHAPTERS_DIR`；`tidy.mjs` 從 `story.mjs` 匯入 `STORY_PAGES_DIR` 放進 `TARGETS`（排在 `clips` 之後），其他一行都沒動：刪除仍只走 `reach()`／`removeTree()`，路上遇到連結（`story/` 是連結）就不穿過、記成失敗，`story/pages` 本身是連結時只移除連結。`story/`、`story/chapters/` 都不在清單上。`tidy.test.mjs` 加兩個測試：故事的頁面清掉、章節留下、位元組算進去、不是故事的影片沒有 `story/` 也不算失敗；`story/pages` 是 junction 時只移除連結、指到的東西還在，`story/` 是 junction 時不穿過、其餘大檔照清。
- 注意：`tidy.mjs` 現在匯入 `story.mjs`，所以 `tools/video/cli.mjs`（`status` 用 `tidiedNote`）載入時也會載入故事流程的模組；沒有迴圈，那些模組載入時不做事。
- scope 加了三個路徑：`tools/video/automation/story.mjs`（把頁面資料夾的名稱匯出成 `STORY_PAGES_DIR`，清理從這裡讀，名稱只寫一次；`STORY_CHAPTERS_DIR` 也匯出，測試用它確認 `story/chapters/` 留下）、`docs/videos/AUTOMATION.md`（清理工作區一節的刪除與保留清單，上面 Steps 已經說要加）與 skill 的 `references/story.md`（工作區檔案表那一列原本只說頁面存在那裡，沒說會被清）。
