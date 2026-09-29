---
id: 2026-09-28-video-page-reads-whole-series-for
title: 影片頁為了找單集漫劇的故事聖經，每分鐘重讀整部作品
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-28T15:24:26Z
completed_at:
branch:
depends_on:
scope:
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
---

# 影片頁為了找單集漫劇的故事聖經，每分鐘重讀整部作品

## Why

`/admin/videos` 的影片頁（`apps/web/components/admin-video-reviews.tsx` 的 `ProjectDetail`）對每一支屬於作品的影片都掛 `OneOffBible`，它用 `useRefresh` 每分鐘讀一次 `GET /admin/video-automation/series/{series_slug}`，只為了看有沒有 `bible` 文件（只有單集漫劇有）。長篇漫劇與品牌故事的影片頁因此每分鐘讀整部作品：品牌故事匯入 100 個故事之後，這一次讀取約 1.2 MB（每集都帶企劃全文），站主打開一支故事影片等它上架時，一小時約 70 MB，而頁面上什麼都不會多。

## Definition of done

- [ ] 長篇漫劇與品牌故事的影片頁，不再每分鐘讀整部作品；單集漫劇的故事聖經照樣顯示、照樣能討論。
- [ ] 測試數得出影片頁對作品的讀取次數。

## Steps

- [ ] 判斷作品類型的辦法：讀一次就記住不是單集漫劇（`series.kind`）就不再讀，或等票 `2026-09-28-video-story-light-series-read` 的輕量讀法，或讓影片摘要帶作品類型（那是 API 的票）。
- [ ] 元件與測試。

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web -- admin-video-reviews
```

## Notes

- 2026-09-28 做品牌故事後台頁（票 `2026-09-28-video-story-admin`）時看到的；那張票的 scope 不含這個檔案，所以另開。作品頁本身對故事作品已經在第一次讀到之後停掉合集清單的讀取（`admin-video-series.tsx` 的 `SeriesPage`）。
