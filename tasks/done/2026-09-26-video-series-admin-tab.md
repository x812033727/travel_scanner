---
id: 2026-09-26-video-series-admin-tab
title: Video series W1: the drama tab on /admin/videos with the series page, the documents to approve and the episode table
status: done
priority: P1
area: web
owner: claude-fable-5-1-video-drama
claimed_at: 2026-09-26T19:53:26Z
created_at: 2026-09-26T17:36:30Z
completed_at: 2026-09-26T19:53:58Z
branch: claude/video-series-admin-tab
depends_on:
  - 2026-09-26-video-series-api
  - 2026-09-26-video-series-review-card-file
scope:
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# Video series W1: the drama tab on /admin/videos with the series page, the documents to approve and the episode table

## Why

站主要漫劇跟教學影片分開一個分頁，在同一頁建作品、核准設定集／總綱／篇章細綱、看 100 集的進度與花費，並在劇本關卡看每集的劇本。設計全文在 `docs/videos/SERIES.md`（站主 2026-09-27 的決定、名稱、流程、資料模型、提示詞規格都在那裡）；分票與順序在它的「分期與票」。

## Definition of done

- [x] `/admin/videos` 三個分頁：教學影片（篩 `format !== "drama"`）、漫劇、設定（`?tab=settings` 深連結保留）；查詢鍵 `series`；`video=` 仍優先；從單集頁返回回到作品頁。
- [x] `admin-video-series.tsx`：作品列表卡與「新的作品」表單（名稱、前提、參考面向、情感線尺度、風格、每集長度、預計集數、每篇集數、開放結局、備註）；作品頁：控制（暫停／繼續、先規劃下一篇、現在開始下一集）、設定集／總綱／每篇細綱可展開（細綱表格：集數、鉤子、衝突、轉折、懸念、伏筆、張力、狀態）、核准／退回＋備註／自己改、集數表（集數、標題、狀態、目前步驟、待審關卡、花費、打開影片）；單集表單與佇列搬來這裡。
- [x] `ScriptBody`：beat_coverage 與連貫性問題在最上面，逐場景【角色】台詞、可展開的鏡頭提示詞；`approveLabels.script`；`gates.script`。
- [x] 五語 `admin.json`（`videoReviews.tabDrama`、`gates.script`、`approveScript`、`videoSeries.*`）；新 tsx 沒有中文（Han 規則）。
- [x] `admin-video-series.test.tsx` 與 `admin-video-reviews.test.tsx`；lint、typecheck、check:i18n 綠。

## Steps

- [x] 分頁與查詢鍵。
- [x] 作品列表、表單、作品頁。
- [x] ScriptBody 與文案。
- [x] 測試。

## How to verify

```bash
cd apps/web && npx vitest run components/admin-video && npm run lint && npm run typecheck && cd ../.. && git add -A && CI=1 npm run check:i18n
```

2026-09-27（claude-fable-5-1-video-drama）：PR #824。單集的「新的漫劇」表單、佇列與單集漫劇影片列表也搬到漫劇分頁；作品表單的風格標籤叫「畫面風格」，避免與單集表單的「風格」同名。查核的「有／弱／無」以碼點對應顏色，tsx 裡不放中文字面（check:i18n 的 Han 規則）。
