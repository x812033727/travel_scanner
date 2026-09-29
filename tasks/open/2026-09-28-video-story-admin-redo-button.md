---
id: 2026-09-28-video-story-admin-redo-button
title: 故事清單上的「重做」按鈕：放棄過的故事再做一次
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-28T16:04:54Z
completed_at:
branch:
depends_on:
  - 2026-09-28-video-story-redo-dropped
scope:
  - apps/web/components/admin-video-stories.tsx
  - apps/web/components/admin-video-stories.test.tsx
  - apps/web/messages
---

# 故事清單上的「重做」按鈕：放棄過的故事再做一次

## Why

後台的故事清單（`apps/web/components/admin-video-stories.tsx`，票 `2026-09-28-video-story-admin`）對「開始做過、影片已放棄」的故事只寫「不能恢復」，因為恢復只給從沒開始過的故事。票 `2026-09-28-video-story-redo-dropped` 會加上重做的 API（有次數上限）；那張票的 Steps 說後台按鈕另開票，就是這張。

## Definition of done

- [ ] 被放棄過、而且 API 允許重做的故事，清單那一列有「重做」按鈕（`content.manage`），按之前先確認並說明會花一次製作的錢；沒有權限時不出現。
- [ ] 超過重做上限或其他拒絕，顯示 API 給的原因。
- [ ] 重做後清單讀回，狀態回到待做；舊影片的連結照樣打得開。
- [ ] 五語文字；`npm run check:i18n` 通過。

## Steps

- [ ] 等 `video-story-redo-dropped` 合併，照它 Notes 寫的端點、權限與拒絕代碼做。
- [ ] 元件與測試（照 `admin-video-stories.test.tsx` 的做法：同一個 `stubFetch`，斷言請求與畫面）。

## How to verify

```bash
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web -- admin-video-stories
```

## Notes

- 現在那一列的狀態是「已略過」（集數 `skipped`、`started_at` 有值）或「影片已放棄」（影片有 `dropped_at`、集數還沒被標成略過），文字是 `admin.videoStories.list.startedSkipped`；判斷在 `storyState` 與清單的 `episode.status === "skipped" && episode.started_at`。
