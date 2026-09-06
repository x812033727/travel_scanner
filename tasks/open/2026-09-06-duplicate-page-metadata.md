---
id: 2026-09-06-duplicate-page-metadata
title: 十三個公開頁裡有九個共用同一組 title 與 description
status: in-progress
priority: P3
area: web
owner: claude-opus-5
claimed_at: 2026-09-06T17:56:45Z
created_at: 2026-09-06T17:32:56Z
completed_at:
branch: claude/ux-batch-3
depends_on: []
scope:
  - apps/web/app/[locale]/search/page.tsx
  - apps/web/app/[locale]/alerts/page.tsx
  - apps/web/app/[locale]/login/page.tsx
  - apps/web/app/[locale]/register/page.tsx
  - apps/web/app/[locale]/trips/page.tsx
  - apps/web/app/[locale]/account/page.tsx
  - apps/web/messages/en/metadata.json
  - apps/web/messages/ja/metadata.json
  - apps/web/messages/ko/metadata.json
  - apps/web/messages/zh-CN/metadata.json
  - apps/web/messages/zh-TW/metadata.json
---

# 十三個公開頁裡有九個共用同一組 title 與 description

## Why

13 個公開頁裡有 9 個共用同一個 `<title>`「Mokaair｜完整旅程比價」與同一句 meta
description：`/`、`/search`、`/alerts`、`/pricing`、`/login`、`/register`、`/trips`、
`/trips/new`、`/account`。只有 `/hotspots`、`/foods`、`/flights/status`、`/labs/airlines`
有自己的。五個語系都一樣。

分頁列上分不出哪個是哪個（長輩開很多分頁時特別明顯），搜尋結果也會被自己洗掉。

## Definition of done

- [x] 每個公開頁有自己的 title 與 description，五個語系齊全。
- [x] `metadata.json` 的鍵名對得起頁面（`searchTitle`／`loginTitle`…）。

## Notes

2026-09-07：`/search`、`/alerts`、`/pricing`、`/login`、`/register`、`/trips`、
`/trips/new`、`/account` 八頁補上 `generateMetadata`；首頁維持原本那組。
`/line/link` 是 OAuth 導轉用的中繼頁，沒有給人看的內容，刻意不補。
