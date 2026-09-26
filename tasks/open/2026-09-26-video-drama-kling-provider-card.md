---
id: 2026-09-26-video-drama-kling-provider-card
title: Video drama: Kling as a third media provider with its own key card
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-26T01:53:48Z
completed_at:
branch:
depends_on:
  - 2026-09-26-video-drama-media-api
  - 2026-09-26-video-drama-media-volume
  - 2026-09-25-run-the-site-s-claude-features
scope:
  - apps/api/app/config.py
  - apps/api/app/admin/service.py
  - apps/api/app/video_media/providers/kling.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
---

# Video drama: Kling as a third media provider with its own key card

## Why

第二期。Kling 3.0 是動作與多鏡連貫最強的替代方案（1080p 每秒約 US$0.112，原生中文音訊），但要新金鑰卡片、官方主機釘住、預付套餐，而卡片相關的檔案正被 `2026-09-25-run-the-site-s-claude-features` 鎖住，所以獨立成票、排在最後。

## Definition of done

- [ ] `PROVIDER_DEFINITIONS` 有 `kling` 卡（base URL＋access key／secret key），`OFFICIAL_PROVIDER_HOSTS` 與 `validate_deployment_security` 的 pinned endpoints 有它，`CONNECTION_TESTED_PROVIDERS` 或 `LOCAL_ONLY_PROVIDERS` 其一。
- [ ] `video_media/providers/kling.py` 與目錄項；設定分頁可選 Kling。
- [ ] 後台面板分類、`fieldMeta`、五語文案照 `.agents/skills/backend-conventions/references/admin-pages.md`「新增一個供應商」。

## Steps

- [ ] API 卡片與釘住 → adapter 與目錄 → 前端與文案 → 測試。

## How to verify

```bash
cd apps/api && uv run pytest tests/test_admin_provider_settings.py tests/test_admin_readiness.py tests/test_video_media_providers.py -q
```

## Notes

設計全文在 `docs/videos/DRAMA.md`（跟 T1 一起合併）；供應商、價格、政策的研究依據也在那裡。
