---
id: 2026-09-28-video-page-reads-whole-series-for
title: 影片頁為了找單集漫劇的故事聖經，每分鐘重讀整部作品
status: done
priority: P3
area: web
owner: claude-fable-5-1-video-page
claimed_at: 2026-09-30T03:49:48Z
created_at: 2026-09-28T15:24:26Z
completed_at: 2026-09-30T04:02:52Z
branch: claude/video-page-series-read-once
depends_on: []
scope:
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
---

# 影片頁為了找單集漫劇的故事聖經，每分鐘重讀整部作品

## Why

`/admin/videos` 的影片頁（`apps/web/components/admin-video-reviews.tsx` 的 `ProjectDetail`）對每一支屬於作品的影片都掛 `OneOffBible`，它用 `useRefresh` 每分鐘讀一次 `GET /admin/video-automation/series/{series_slug}`，只為了看有沒有 `bible` 文件（只有單集漫劇有）。長篇漫劇與品牌故事的影片頁因此每分鐘讀整部作品：品牌故事匯入 100 個故事之後，這一次讀取約 1.2 MB（每集都帶企劃全文），站主打開一支故事影片等它上架時，一小時約 70 MB，而頁面上什麼都不會多。

## Definition of done

- [x] 長篇漫劇與品牌故事的影片頁，不再每分鐘讀整部作品；單集漫劇的故事聖經照樣顯示、照樣能討論。
- [x] 測試數得出影片頁對作品的讀取次數。

## Steps

- [x] 判斷作品類型的辦法：讀一次就記住不是單集漫劇（`series.kind`）就不再讀，或等票 `2026-09-28-video-story-light-series-read` 的輕量讀法，或讓影片摘要帶作品類型（那是 API 的票）。
- [x] 元件與測試。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web -- admin-video-reviews
```

## Notes

- 2026-09-28 做品牌故事後台頁（票 `2026-09-28-video-story-admin`）時看到的；那張票的 scope 不含這個檔案，所以另開。作品頁本身對故事作品已經在第一次讀到之後停掉合集清單的讀取（`admin-video-series.tsx` 的 `SeriesPage`）。
- 2026-09-30（claude-fable-5-1-video-page）認領時工具說 scope 與 `2026-09-28-drama-preloaded-document-approval-order`（codex-ten-drama）重疊，重疊的只有 `admin-video-reviews.test.tsx`；那張票的 PR #978 已在 2026-09-29 合併、認領超過 24 小時卻沒 `done`，所以用 `--force` 接手。這裡只在測試檔加一個新測試，不動它的測試；那張票自己的 `done` 留給它的持有者。
- 做法：選了「讀一次就記住」，不必等 API 的票。`SeriesSummary.kind`（`apps/api/app/video_automation/schemas.py`）是必有欄位、預設 `"series"`，所以每個作品的回應都帶 kind，可靠；只有更舊、沒有 kind 的回應才退回看有沒有 `bible` 文件。`OneOffBible` 第一次讀到不是 `one-off` 就記下這個 slug（以 slug 為準，換成別的作品會重讀），並停掉自己的計時器。它不再經過 `useRefresh`（那個 hook 停不下來，又在 scope 外的 `admin-video-review-card.tsx`），改在元件裡寫同樣的 effect，多一個 `settled` 條件。單集漫劇照舊每分鐘讀，故事聖經與討論串照常更新；按核准後的 `onChanged` 也照舊重讀。
- 測試 `reads a long series or a brand story once…` 用假計時器快轉三分鐘：長篇（kind `series`）、品牌故事（kind `story`）、沒有 kind 的舊回應都只讀一次作品，影片頁本身照樣每分鐘讀；單集漫劇讀四次、故事聖經還在。把舊元件放回去跑這個測試會失敗（`expected 4 to be 1`），確認它真的數得到。
- 驗證：`cd apps/web && npx vitest run components/admin-video-reviews.test.tsx`（26 過）、`npm run typecheck:web`、`npm run lint:web`、`npm run check:tasks`。
