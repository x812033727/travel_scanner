---
id: 2026-11-14-admin-video-pools-tab-producible-themes
title: Admin video pools tab: producible themes, audience scores and pool expansion history
status: done
priority: P2
area: web
owner: claude-opus-5-5-pool-audience
claimed_at: 2026-11-14T18:12:44Z
created_at: 2026-11-14T18:12:43Z
completed_at: 2026-11-14T18:28:16Z
branch: claude/determined-lamport-1dky28
depends_on: []
scope:
  - tools/video/pool-admin
  - tools/video/curio/pool/cli.mjs
  - tools/video/so-thats-why/pool/cli.mjs
  - apps/api/app/video_pools
  - apps/api/app/main.py
  - apps/api/app/i18n.py
  - apps/api/tests/test_video_pools.py
  - apps/web/components/admin-video-pools.tsx
  - apps/web/components/admin-video-pools.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/components/admin-video-shorts.test.tsx
  - apps/web/lib/video-pools-copy.ts
  - apps/web/lib/video-pools-messages
  - docs/videos/history-curiosity/pool/README.md
  - docs/videos/so-thats-why/pool/README.md
---

# Admin video pools tab: producible themes, audience scores and pool expansion history

## Why

站主 2026-11-14：後台要看得到兩個題目池的成題資訊（題案、獨立觀眾評分與改進紀錄）和擴池資訊。確認的做法：放在影片後台分頁、只放原文內容但介面五語、每次池子 build 自動重產資料包。AI 劇劇本另開第二階段。

## Definition of done

- [x] `/admin/videos?tab=pools`：系列切換、總覽數字、成題列表（狀態／分類／最低分／搜尋、分頁）、題案詳情（評分紀錄與改動、章節、素材審視、風險）、擴池紀錄（批次與存檔點）。
- [x] 資料包 `apps/api/app/video_pools/data/pools.json` 由 `tools/video/pool-admin/bundle.mjs` 產生，兩池 `cli.mjs build` 自動重產，`test:tools` 檢查一致。
- [x] API 唯讀、`content.read`、缺資料回 503；pytest、vitest 涵蓋。

## How to verify

```bash
node tools/video/pool-admin/bundle.mjs check
cd apps/api && uv run pytest tests/test_video_pools.py
cd apps/web && npx vitest run components/admin-video-pools.test.tsx components/admin-video-shorts.test.tsx
```

## Notes

- `apps/web/components/admin-video-reviews.tsx` 也在幾張 2026-10 停滯數百小時的舊票範圍內；這裡只在分頁清單加一項。
- `admin-video-shorts.test.tsx` 寫死了影片後台的分頁順序，加分頁時要一起改。
- 下一階段：AI 劇劇本分頁（太奶奶、重天取奇、歐德江湖、零根妖族、修仙獎勵），照同樣的資料包模式。
