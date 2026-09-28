---
id: 2026-09-28-video-shorts-d0-design-the-shorts
title: Video shorts D0: design the Shorts tab, its three content lines and the tickets
status: done
priority: P2
area: docs
owner: claude-fable-5-1-shorts
claimed_at: 2026-09-28T02:55:24Z
created_at: 2026-09-28T02:55:04Z
completed_at: 2026-09-28T03:32:15Z
branch: claude/shorts-area-planning-28f89d
depends_on: []
scope:
  - docs/videos/SHORTS.md
---

# Video shorts D0: design the Shorts tab, its three content lines and the tickets

## Why

站主 2026-09-28 要求「規劃 Shorts 區」。PR #871 已經有本機的 Shorts 試片產線（`tools/video/shorts`、`docs/videos/ai-shorts`），但後台沒有 Shorts 的位置：看片要到開發機上找檔案，排程、成效、花費都是 repo 外的 CSV，上架要站主在 Studio 填全部欄位。站主一貫的要求是一切接到後台、不碰命令列、只決定最少的事。

這張票交付設計文件與分票，不寫程式。

## Definition of done

- [x] 站主的四個決定問到並寫下來：Shorts 區是後台 `/admin/videos` 的分頁；內容線是實測、長片精華、漫劇直式短篇；全自動；製作兩條都留、分期做。
- [x] `docs/videos/SHORTS.md`：現況與缺口、名稱、一支 Shorts 的一生、三條內容線、分頁的每個區塊、自動品管 12 項與伺服器規則、排片與時段、上架（授權、稽核前後）、成效與每週報告、花費、資料模型、端點、工具端、政策與依據、風險、站主要做的事、分期與票、還要站主決定的事。
- [x] 15 張票（`2026-09-28-video-shorts-*`）與兩張順手發現的小票，scope 列到檔案，`npm run check:tasks` 過。
- [x] YouTube 的規則以 2026-09-28 讀到的官方頁為準，查不到或互相矛盾的地方在文件裡標出來。

## Steps

- [x] 盤點現況：#871 的工具與文件、後台三個分頁、伺服器的影片模組、工人的迴圈、開著的 PR 與平行的 session。
- [x] 問站主四個決定。
- [x] 三個背景調查：YouTube 官方規則、伺服器資料模型與端點、後台元件與工具。
- [x] 寫設計文件與票。

## How to verify

```bash
npm run check:tasks
npm run tasks -- list --area api | grep video-shorts
```

讀 `docs/videos/SHORTS.md` 的「分期與票」，每一列在 `tasks/open/` 都有對應的檔案。

## Notes

- 開工時平行的工作線：PR #870（大改 `/admin/videos` 的元件、設定與 `video_reviews`，佔了遷移 0105–0108）；品牌故事影片（票 `2026-09-28-video-story-*`，每天兩支 16:9 長片，用漫劇產線）；Codex 的 PR #880（六集長片各切兩支 Shorts，本機做好）。三者都寫進了設計文件的相依與風險。
- 親自核對過的官方頁：開發人員政策（自動上傳的同意、最後決定權、衍生指標、資料保存）、衍生指標的增修條款、影片資源（`publishAt`、`fileDetails.fileName`、`containsSyntheticMedia`、`viewCount`）、Analytics 的指標與維度、營利計畫的門檻與 2027-02-01 的改制、營利政策、相關影片、A/B 測試、三分鐘 Shorts。其餘由研究代理讀取，文件裡照它回報的寫。
- `https://mokaair.com/en/privacy` 在 2026-09-28 還沒有 YouTube API 段落，所以稽核申請還沒辦法送。
- 沒有連到正式主機、沒有部署、沒有碰任何站上的資料。
