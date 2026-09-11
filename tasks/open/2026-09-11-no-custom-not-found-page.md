---
id: 2026-09-11-no-custom-not-found-page
title: 全站沒有自訂的找不到頁面
status: in-progress
priority: P1
area: web
owner: claude-opus-5
claimed_at: 2026-09-11T13:17:20Z
created_at: 2026-09-11T03:20:59Z
completed_at:
branch: claude/mokaair-website-access-k7xiku
depends_on: []
scope:
  - apps/web/app/[locale]/not-found.tsx
  - apps/web/messages/en/common.json
  - apps/web/messages/ja/common.json
  - apps/web/messages/ko/common.json
  - apps/web/messages/zh-CN/common.json
  - apps/web/messages/zh-TW/common.json
---

# 全站沒有自訂的找不到頁面

## Why

`find apps/web/app -name "not-found*"` 沒有任何結果。任何打錯的網址、任何失效的舊連結、任何被刪掉的行程分享連結，都會落到 Next.js 的預設 404 畫面：純英文、沒有站台導覽、沒有回首頁的路。

`app/[locale]/error.tsx:8-13` 的存在正是為了避免這件事——它接住渲染錯誤並給出一個像樣的頁面——但 404 不走 error boundary，所以沒被涵蓋。

具體會踩到的路徑之一：`/flights` 本身沒有 page（`app/[locale]/flights/` 底下只有 `status/`），任何人從舊連結或手打進來就是預設 404。

## Definition of done

- [ ] `/zh-TW/<不存在的路徑>` 顯示站台自己的 404 頁，有頁首、有回首頁的連結。
- [ ] 五語系都正確。

## Steps

- [ ] 新增 `app/[locale]/not-found.tsx`，版面沿用 `error.tsx` 的作法。
- [ ] 文案放 `messages/*/common.json`。
- [ ] 給幾個實際有用的出口：首頁、探索、我的旅程。
- [ ] 確認 `/flights` 這類「有子路徑但沒有自己 page」的情況也會落到這頁。

## How to verify

```bash
cd apps/web && npm run check:i18n && npm run build
```

手動：`/zh-TW/nope`、`/ja/nope`、`/en/flights` 各開一次。

## Notes

- 站主刻意關閉的四個功能（`/alerts`、`/flights/status`、`/labs/airlines`、`/pricing`）走的是另一套「暫停開放」頁，不是 404，不要混在一起。
