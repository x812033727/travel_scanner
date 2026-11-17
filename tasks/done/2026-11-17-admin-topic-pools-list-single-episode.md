---
id: 2026-11-17-admin-topic-pools-list-single-episode
title: Admin topic pools list single-episode cores
status: done
priority: P2
area: web
owner: claude-fable-heimao-topics
claimed_at: 2026-11-17T12:28:37Z
created_at: 2026-11-17T12:28:25Z
completed_at: 2026-11-17T12:42:59Z
branch:
depends_on: []
scope:
  - tools/video/pool-admin
  - apps/api/app/video_pools
  - apps/api/tests/test_video_pools.py
  - apps/web/components/admin-video-pools.tsx
  - apps/web/components/admin-video-pools.test.tsx
  - apps/web/lib/video-pools-messages
  - apps/web/e2e/admin-video-pools-cores.spec.ts
---

# Admin topic pools list single-episode cores

## Why

後台題目池頁只列長題案（`themes.json`），分類選單也從長題案算。奇聞池的「商業與品牌奇聞」81 題入選題全是單集題、沒有長題案，
所以站主在後台完全看不到這一類；其他八類的單集題也一樣沒有入口。奇聞池入選的單集題有 1300 題，856 題評過分、298 題總分過 6.5。

## Definition of done

- [x] 後台題目池頁多一個「單集題」檢視，列出奇聞池入選的單集題，可依狀態、分類、最低分、關鍵字篩選，依排名排序。
- [x] 分類選單裡有「商業與品牌奇聞」，選了看得到撲克牌黑桃 A、十字螺絲等題與分數。
- [x] 原來如此系列在這個檢視是空的（它的單題沒有評分），頁面顯示空狀態而不是錯誤。

## Steps

- [x] `tools/video/pool-admin/bundle.mjs`：每個系列多 `cores` 與三個計數；重建 `pools.json`。
- [x] `apps/api/app/video_pools/`：`CoreSummary`、`CorePage`、`list_cores`、`GET /{series}/cores`。
- [x] `apps/web/components/admin-video-pools.tsx` 與五語系文案：`cores` 檢視。
- [x] 三處測試；用假 API 在瀏覽器實際看一次。

## How to verify

```bash
node tools/video/pool-admin/bundle.mjs check && node --test tools/video/pool-admin/bundle.test.mjs
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_pools.py
npm run lint:web && npm run check:i18n && npm run typecheck:web
cd apps/web && npx vitest run components/admin-video-pools.test.tsx
```

## Notes

- 不部署；合併後要部署後台才看得到。
- 資料包從 2.4 MB 長到 3.9 MB（1300 題單集題）。API 每次請求都重讀並驗證整份資料包，這是既有設計；`bundle.test.mjs` 設了 12 MiB 的上限，
  超過就該改成分頁載入或加快取。
- 單集題的開場與「這集會揭曉」直接放在列表回應裡，展開時不另外打 API。
- 瀏覽器驗收：`apps/web/e2e/admin-video-pools-cores.spec.ts` 用打包好的資料包當假 API，桌機與手機寬度都過。
  這個環境的 `next dev` 第一次啟動會先印一段升級提醒就結束，再跑一次才會起來；Playwright 要指定內建的 Chromium 才跑得動，設定檔沒有進 repo。
- 搜尋框的標籤沿用題案檢視的「搜尋片名、追問或題案編號」，在單集題檢視實際比對的是代號、題目與開場。
