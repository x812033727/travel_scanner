---
id: 2026-10-05-stock-photo-source-endpoint
title: Stock photo source endpoint: Pexels and Pixabay search and fetch into the media store, keys server-only
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-05T16:08:26Z
completed_at:
branch:
depends_on:
  - 2026-10-05-media-locate-subject-boxes
scope:
  - apps/api/app/config.py
  - apps/api/app/admin/service.py
  - apps/api/app/video_media/stock.py
  - apps/api/tests/test_video_media_stock.py
  - apps/api/app/video_media/admin_api.py
  - apps/api/app/video_media/schemas.py
  - apps/api/app/video_media/storage.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - docs/videos/ILLUSTRATED.md
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Stock photo source endpoint: Pexels and Pixabay search and fetch into the media store, keys server-only

## Why

The pipeline has no stock footage or photos at all; the travel site's guides are drawn as
dark slides or AI pictures while Pexels and Pixabay hold real photos of Seoul, Busan and
Jeju under licences that allow commercial use. Vendor keys never reach the tool, so the
source is a server endpoint that searches and fetches into the media store, registered like
any provider (`backend-conventions`: Settings field, provider definition, connection test,
category, ownership, official host pin).

## Definition of done

- [ ] `POST /video/media/stock/search {query, orientation, per_page}` returns candidates with
      photographer, page URL and licence; `POST /video/media/stock/fetch {slug, provider, id}`
      downloads the original into the media store and returns `{sha256, width, height, credit:
      {author, url, license, provider}}`. Not a `video_media_jobs` row (the kind CHECK stays
      image / clip / music).
- [ ] Keys are server-only (`pexels_api_key`, `pixabay_api_key`), tested by the settings page's
      connection test, pinned to `api.pexels.com` and `pixabay.com`.
- [ ] The provider shows on the settings page in the right category with five-locale labels.

## Steps

- [ ] `config.py`, `admin/service.py` (`ProviderDefinition`, `CONNECTION_TESTED_PROVIDERS`),
      `OFFICIAL_PROVIDER_HOSTS`; the existing provider enumeration tests (find with
      `grep -rl CONNECTION_TESTED_PROVIDERS apps/api/tests apps/web/components` and add them to scope).
- [ ] `video_media/stock.py` + tests with `httpx.MockTransport`; routes and schemas; `storage.py`
      accepts the fetched original.
- [ ] `admin-settings-panel.tsx` category + `admin.json` ×5 labels + ownership; `ILLUSTRATED.md`.
- [ ] Receipt increment by an independent agent (admin.json ×5).

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_media_stock.py tests/test_admin_readiness.py -q
npm run lint:web && npm run check:i18n && npm run typecheck:web
node tools/video/long-form/cli.mjs check
```

## Notes

- Bound: `apps/web/messages/*/admin.json`.
- Same plumbing as `2026-09-26-video-drama-kling-provider-card`; whichever lands first, the
  other rebases.
- Attribution is written by `2026-10-05-stock-photo-slides-and-attribution`.
