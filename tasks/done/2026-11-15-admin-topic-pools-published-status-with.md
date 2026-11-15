---
id: 2026-11-15-admin-topic-pools-published-status-with
title: Admin topic pools: published status with YouTube IDs per produced episode
status: done
priority: P2
area: web
owner: claude-opus-5-5-pool-audience
claimed_at: 2026-11-15T04:22:29Z
created_at: 2026-11-15T04:22:27Z
completed_at: 2026-11-15T04:27:49Z
branch: claude/determined-lamport-1dky28
depends_on: []
scope:
  - tools/video/pool-admin
  - apps/api/app/video_pools
  - apps/api/tests/test_video_pools.py
  - apps/web/components/admin-video-pools.tsx
  - apps/web/components/admin-video-pools.test.tsx
  - apps/web/lib/video-pools-messages
---

# Admin topic pools: published status with YouTube IDs per produced episode

## Why

站主 2026-11-15：題目池裡也要看得到上架狀態——是否上架、上架的 YouTube ID，篩選那邊可以選要不要看上架的清單。

## Definition of done

- [x] 題目池分頁「檢視」多一個「上架狀態」：已上架／未上架／全部篩選與搜尋，每集顯示 YouTube ID（連結）、來源、預定公開時間、製作階段與對應題號。
- [x] 資料包加上每池的已製作集數（各集總表 catalog.json 對回題目池：奇聞用 production.locators 的集數資料夾，原來如此用 prior_decision.episode 的集數代號）。
- [x] `GET /admin/video-pools/{series}/episodes` 以站台 `video_projects` 的 YouTube ID 為準（撤下的不算），查不到才用總表的值。

## How to verify

```bash
node --test tools/video/pool-admin/bundle.test.mjs
cd apps/api && uv run pytest tests/test_video_pools.py
cd apps/web && npx vitest run components/admin-video-pools.test.tsx
```

## Notes

- 題案（themes）本來就排除已製作的題，所以上架狀態列在集數層級，不掛在題案卡上。
- `catalog.json` 由 `docs/videos/ai-drama-drive/catalog.py` 重產；重產後要跑 `node tools/video/pool-admin/bundle.mjs build`，否則 `test:tools` 會擋。
