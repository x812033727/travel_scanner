---
id: 2026-09-28-video-story-admin-redo-button
title: 故事清單上的「重做」按鈕：放棄過的故事再做一次
status: in-progress
priority: P3
area: web
owner: claude-opus-5-5-story-redo-button
claimed_at: 2026-10-01T11:29:28Z
created_at: 2026-09-28T16:04:54Z
completed_at:
branch: claude/story-redo-button
depends_on:
  - 2026-09-28-video-story-redo-dropped
scope:
  - apps/web/components/admin-video-stories.tsx
  - apps/web/components/admin-video-stories.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# 故事清單上的「重做」按鈕：放棄過的故事再做一次

## Why

後台的故事清單（`apps/web/components/admin-video-stories.tsx`，票 `2026-09-28-video-story-admin`）對「開始做過、影片已放棄」的故事只寫「不能恢復」，因為恢復只給從沒開始過的故事。票 `2026-09-28-video-story-redo-dropped` 會加上重做的 API（有次數上限）；那張票的 Steps 說後台按鈕另開票，就是這張。

## Definition of done

- [x] 被放棄過、而且 API 允許重做的故事，清單那一列有「重做」按鈕（`content.manage`），按之前先確認並說明會花一次製作的錢；沒有權限時不出現。
- [x] 超過重做上限或其他拒絕，顯示 API 給的原因。
- [x] 重做後清單讀回，狀態回到待做；舊影片的連結照樣打得開。
- [x] 五語文字；`npm run check:i18n` 通過。

## Steps

- [x] 等 `video-story-redo-dropped` 合併，照它 Notes 寫的端點、權限與拒絕代碼做。
- [x] 元件與測試（照 `admin-video-stories.test.tsx` 的做法：同一個 `stubFetch`，斷言請求與畫面）。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web -- admin-video-stories
```

## Notes

- 現在那一列的狀態是「已略過」（集數 `skipped`、`started_at` 有值）或「影片已放棄」（影片有 `dropped_at`、集數還沒被標成略過），文字是 `admin.videoStories.list.startedSkipped`；判斷在 `storyState` 與清單的 `episode.status === "skipped" && episode.started_at`。

### 做完的紀錄（2026-10-01，claude-opus-5-5-story-redo-button）

- **認領用了 `--force`，scope 也縮小了**：原本 scope 是整個 `apps/web/messages`，與四張 `review` 票重疊。這張票只改五個 `admin.json`，所以 scope 改成那五個檔；之後仍重疊的兩張都是過期、PR 已合併的認領：`codex-ten-drama` 的 `2026-09-28-drama-preloaded-document-approval-order`（PR #978，2026-09-29 合併）與 `claude-fable-5-1-video-languages` 的 `2026-09-27-video-drama-room-withdraw-a-one`（PR #870，2026-09-28 合併）。原本另外重疊的 `claude-fable-5-1` 兩張（PR #553–#565，2026-09-19 合併）只碰 `newTrip.json`、`community.json`，縮小 scope 後就不重疊。
- **按鈕何時出現**：`episode.status === "skipped"` 且 `started_at` 有值（API 的「被放棄」），而且集數的 slug 還沒用完重做次數。API 不回剩幾次，所以讀 slug：`storyRedo` 認 `-redo<n>`（n 從 1、沒有前導 0，與 `series.py` 的 `REDO_NUMBER` 相同），`STORY_REDO_LIMIT = 1` 寫在元件裡並註明來源；API 改上限時兩邊要一起改。只有 `content.manage` 看得到按鈕（`canManage`，與略過、恢復相同）。「影片已放棄」狀態（影片有 `dropped_at`、集數還沒標成略過）API 會拒絕，所以不出按鈕。
- **確認**：`window.confirm` 寫出故事代號、標題、「再花一次製作的錢（圖片、旁白）」、只能重做一次、舊影片留著從「上一支影片」打開。取消就不送。
- **拒絕**：走清單原本的 `act`，錯誤顯示 `admin.videoSeries.actionError`（「沒有做：{message}」），message 是 API 的 detail，所以 `video_series_redo_limit` 等拒絕原因原樣顯示。
- **讀回**：成功後呼叫與略過、恢復相同的 `onChanged`（PR #1070 的 `?beats=summary` 輕量讀取）；測試斷言重做後只多一次 `?beats=summary` 的讀取，狀態變「待做」。開著的企劃因為列的 slug、狀態變了會照 `useStoryPlan` 的規則重讀。
- **舊影片**：重做後那一列的 `video` 是空的（新代號還沒開始）。slug 有 `-redo<n>` 的列多一顆「上一支影片」，打開被取代的那支：`-redo1` 打開計畫 slug，`-redo2` 打開 `-redo1`。這顆不需要權限（只是打開影片頁）。
- **文字**：`admin.videoStories.list` 加 `redo`、`redoable`、`redoConfirm`、`earlierVideo`；`startedSkipped` 現在只用在「已經重做過又放棄」的列，文字改成「不能再重做、要再做請用新的故事代號匯入」（原本的「不能恢復」對還能重做的故事已經不對）。鍵名沒改，站主若覆寫過舊句子，覆寫會照舊蓋在新意思上，PR 說明有寫。
- 驗證：`npx vitest run components/admin-video-stories.test.tsx`（19 個全過，新增三個：`storyRedo` 的單元測試、重做整條流程含取消／讀回／上一支影片、API 拒絕的原因；讀者測試加上看不到「重做」）、`npm run typecheck:web`、`npm run lint:web`、`npm run check:i18n`、`npm run check:tasks` 都通過。只在部署後生效。
