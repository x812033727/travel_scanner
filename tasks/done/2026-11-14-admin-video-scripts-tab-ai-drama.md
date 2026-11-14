---
id: 2026-11-14-admin-video-scripts-tab-ai-drama
title: Admin video scripts tab: AI drama briefs, scripts, storyboards and series documents
status: done
priority: P2
area: web
owner: claude-opus-5-5-pool-audience
claimed_at: 2026-11-14T18:40:00Z
created_at: 2026-11-14T18:28:18Z
completed_at: 2026-11-14T18:28:19Z
branch: claude/determined-lamport-1dky28
depends_on: []
scope:
  - tools/video/drama-admin
  - apps/api/app/video_dramas
  - apps/api/app/main.py
  - apps/api/app/i18n.py
  - apps/api/tests/test_video_dramas.py
  - apps/web/components/admin-video-dramas.tsx
  - apps/web/components/admin-video-dramas.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-shorts.test.tsx
  - apps/web/lib/video-dramas-copy.ts
  - apps/web/lib/video-dramas-messages
  - docs/videos/drama/README.md
---

# Admin video scripts tab: AI drama briefs, scripts, storyboards and series documents

## Why

站主 2026-11-14：後台要看得到 AI 劇的劇本資訊；劇本先只放 AI 劇，介面五語、內容放原文。

## Definition of done

- [x] `/admin/videos?tab=scripts`：選劇、分集列表（集數、改寫版、標題、片長、有哪些文件、搜尋）、單集閱讀（簡介、劇本、分鏡、審稿切換）、系列文件（大綱、季綱、設定、README）。
- [x] 資料包 `apps/api/app/video_dramas/data/`（index.json 加每部一檔，index 釘住內容 sha256），由 `tools/video/drama-admin/bundle.mjs` 產生，`test:tools` 檢查一致。
- [x] API 唯讀、`content.read`、資料缺漏或內容對不上回 503；pytest、vitest 涵蓋。

## How to verify

```bash
node tools/video/drama-admin/bundle.mjs check
cd apps/api && uv run pytest tests/test_video_dramas.py
cd apps/web && npx vitest run components/admin-video-dramas.test.tsx
```

## Notes

- 規則（`production/RULES.md`）與教訓檔常被其他 session 修改，刻意不放進資料包，免得每次改教訓都讓 CI 失敗。
- 改任何一集的 brief／script／storyboard／review 或系列企劃資料夾最上層的 Markdown 後，要跑 `node tools/video/drama-admin/bundle.mjs build` 並一起提交；`docs/videos/drama/README.md` 已寫明。
- 資料包約 12MB，最大單檔約 5MB（種田），API 每次只讀一部劇的檔案。
- 認領時 `tasks` 工具回報範圍與 2026-10-12、10-13、10-19、10-30、11-02 幾張票重疊（`main.py`、`i18n.py`、`admin-video-reviews.tsx`），那些票都已停滯數百小時，沒有對應的進行中工作；這裡只新增 router 掛載、錯誤訊息與一個分頁項目。
