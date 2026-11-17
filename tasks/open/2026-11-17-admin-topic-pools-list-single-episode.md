---
id: 2026-11-17-admin-topic-pools-list-single-episode
title: Admin topic pools list single-episode cores
status: in-progress
priority: P2
area: web
owner: claude-fable-heimao-topics
claimed_at: 2026-11-17T12:28:37Z
created_at: 2026-11-17T12:28:25Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/pool-admin
  - apps/api/app/video_pools
  - apps/api/tests/test_video_pools.py
  - apps/web/components/admin-video-pools.tsx
  - apps/web/components/admin-video-pools.test.tsx
  - apps/web/lib/video-pools-messages
---

# Admin topic pools list single-episode cores

## Why

後台題目池頁只列長題案（`themes.json`），分類選單也從長題案算。奇聞池的「商業與品牌奇聞」81 題入選題全是單集題、沒有長題案，
所以站主在後台完全看不到這一類；其他八類的單集題也一樣沒有入口。奇聞池入選的單集題有 1300 題，856 題評過分、298 題總分過 6.5。

## Definition of done

- [ ] 後台題目池頁多一個「單集題」檢視，列出奇聞池入選的單集題，可依狀態、分類、最低分、關鍵字篩選，依排名排序。
- [ ] 分類選單裡有「商業與品牌奇聞」，選了看得到撲克牌黑桃 A、十字螺絲等題與分數。
- [ ] 原來如此系列在這個檢視是空的（它的單題沒有評分），頁面顯示空狀態而不是錯誤。

## Steps

- [ ] `tools/video/pool-admin/bundle.mjs`：每個系列多 `cores` 與三個計數；重建 `pools.json`。
- [ ] `apps/api/app/video_pools/`：`CoreSummary`、`CorePage`、`list_cores`、`GET /{series}/cores`。
- [ ] `apps/web/components/admin-video-pools.tsx` 與五語系文案：`cores` 檢視。
- [ ] 三處測試；用假 API 在瀏覽器實際看一次。

## How to verify

```bash
node tools/video/pool-admin/bundle.mjs check && node --test tools/video/pool-admin/bundle.test.mjs
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_pools.py
npm run lint:web && npm run check:i18n && npm run typecheck:web
cd apps/web && npx vitest run components/admin-video-pools.test.tsx
```

## Notes

- 不部署；合併後要部署後台才看得到。
