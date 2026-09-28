---
id: 2026-09-28-video-story-admin
title: 後台的故事清單、匯入表單、每日支數與上架時段
status: in-progress
priority: P2
area: web
owner: claude-opus-5-5-video-story-admin
claimed_at: 2026-09-28T14:27:24Z
created_at: 2026-09-28T03:31:15Z
completed_at:
branch: claude/video-story-admin
depends_on:
  - 2026-09-28-video-story-api-series-kind
scope:
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/components/admin-video-stories.tsx
  - apps/web/components/admin-video-stories.test.tsx
  - apps/web/app/api/admin
  - apps/web/messages
---

# 後台的故事清單、匯入表單、每日支數與上架時段

## Why

站主的原則是一切在後台做、不碰命令列。品牌故事第一期用主機指令匯入清單（票 `2026-09-28-video-story-api-series-kind`），用既有的作品頁暫停與略過集數；這樣能上線，但站主看不到清單全貌，也改不了每天幾支。

## Definition of done

- [ ] `/admin/videos` 的漫劇分頁裡，故事作品有自己的清單：每一列是一個故事（代號、標題、分類、排程日與時段、狀態、影片連結），可以篩選分類與狀態。
- [ ] 清單上方顯示今天已開始幾支、每日上限、同時進行幾支、「可以上架」緩衝幾支，以及現在不開新故事的原因（如果有）。
- [ ] 有 `settings.manage` 的帳號可以改每日支數、暫停作品、略過或恢復一個還沒開始的故事；沒有權限時看得到但不能改，並說明需要什麼角色。
- [ ] 匯入表單：貼上或上傳 `stories.json`，先顯示試跑結果（新增、更新、略過的列數與問題），確認後才寫入。
- [ ] 「可以上架」卡片對故事預填下一個空的上架時段（12:00 或 20:00，台北時間）。
- [ ] 五個語系的文字都有；`npm run check:i18n` 通過。

## Steps

- [ ] 伺服器端如果缺端點（清單、改每日支數、匯入），在這張票的 web 轉送路由加；API 本身缺的另開票。
- [ ] 元件與測試。
- [ ] 五語文字。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
```

本機沒有 API 時預覽後台頁的方法見記憶「YouTube channel link」與 skill `web-i18n-e2e`。

## Notes

- PR #870 大改了 `admin-video-series.tsx` 與設定元件，Shorts 那條線也要在 `/admin/videos` 加分頁（`docs/videos/SHORTS.md`）；開工前先查誰在動同一批檔案。
- 新的後台頁或分頁要做的登記見 skill `backend-conventions`。
- 分鏡審核卡片的分頁聯絡表不用這張票做：PR #895 合併時已經一起做了（`admin-video-review-card.tsx` 的 `StoryboardBody`，測試在 `admin-video-storyboard-pages.test.tsx`）。
- 匯入指令多了 `--limit` 與 `--episodes-per-day`，作品多了 `look` 欄位（票 `api-series-kind`）；匯入表單要能選只匯入前幾個。
- 2026-09-28 認領（claude-opus-5-5-video-story-admin），用了 `--force`：`claim` 先因為相依的票 `2026-09-28-video-story-api-series-kind` 還在 `in-progress` 而拒絕。它的 PR #910 已在 2026-09-28T11:49Z 合併進 main（`3156370b8`），只剩結案的 PR #923 還開著。`--force` 同時蓋過了 scope 的重疊：四張 `review` 狀態的 PR #870 票（`video-drama-room-web`、`video-drama-room-withdraw-a-one`、`video-languages-web`、`video-split-settings-web`；#870 在 06:38Z 合併，遠端分支已刪，只是沒人跑 `done`），以及兩張 9 月過期的票（`ask-origin-airport-at-trip-creation`、`display-card-promises-language`，只持有 `newTrip.json` 與 `community.json`，這張票不碰）。那些票都沒有動。分支 `claude/video-story-admin` 從 PR #936 的分支 `claude/video-story-admin-import-api`（草稿，匯入與恢復的端點）開，再併 main；#936 合併之前，這張票的 PR 會帶著它的 commit。
