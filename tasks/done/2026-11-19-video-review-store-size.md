---
id: 2026-11-19-video-review-store-size
title: Owner sets the review store size from the admin
status: done
priority: P1
area: web
owner: claude-opus-5-5-review-store
claimed_at: 2026-11-19T00:12:04Z
created_at: 2026-11-19T00:11:39Z
completed_at: 2026-11-19T01:40:32Z
branch: claude/kind-mccarthy-5m28jo
depends_on: []
scope:
  - apps/api/app/video_reviews/store_view.py
  - apps/web/components/admin-settings-panel.test.tsx
  - docs/videos/HANDS-OFF.md
  - apps/api/app/admin/service.py
  - apps/api/app/video_reviews/admin_api.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/tests/test_video_review_store.py
  - apps/web/components/admin-video-review-store.tsx
  - apps/web/components/admin-video-review-store.test.tsx
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/lib/video-review-store-copy.ts
  - apps/web/lib/video-review-store-messages
  - .env.example
  - apps/api/tests/test_migration_0144_video_runpod_sessions.py
---

# Owner sets the review store size from the admin

## Why

The preview store's cap (`video_review_max_total_bytes`) lived only in the host's `.env`; it had
been raised by hand to 30, 40 and 60 GB, and once the container was not rebuilt after the edit
(2026-10-24). When it fills, new previews get 507. Owner, 2026-11-19: set it from the admin, see
how full it is, and make it 80 GB.

## Definition of done

- [x] /admin/videos → 設定 shows 審片空間: used of limit, a bar, the host disk's free space.
- [x] A settings manager types the limit in whole GB (1–500) and it applies at once.

## Steps

- [x] `video_reviews` provider (always enabled, no secrets) owning `video_review_max_total_bytes`;
      integer check in `_validate_provider_values`.
- [x] `GET /admin/videos/store` (`content.read`): used, cap, file cap, disk free/total.
- [x] `admin-video-review-store.tsx` card on the video settings tab; copy in
      `lib/video-review-store-messages/` (not messages/*/admin.json, which the duration review binds).
- [x] The generic settings page does not list `video_reviews`.
- [x] HANDS-OFF.md and .env.example say the admin value wins.

## How to verify

After the deploy: /admin/videos → 設定 → 審片空間, type 80, save; the card reads 上限 80 GB.

## Notes

- Claimed with `--force` (owner approved): older claims list admin/service.py, the video review
  API and the settings panel.
- The card shows decimal GB (80 typed reads back as 80 GB), unlike the backup card's binary sizes.
- `ReviewStoreView` lives in `video_reviews/store_view.py` because `schemas.py` is review-bound.
