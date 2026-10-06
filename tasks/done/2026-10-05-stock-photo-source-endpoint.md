---
id: 2026-10-05-stock-photo-source-endpoint
title: Stock photo source endpoint: Pexels and Pixabay search and fetch into the media store, keys server-only
status: done
priority: P2
area: api
owner: claude-fable-5-1-stock
claimed_at: 2026-10-05T16:51:21Z
created_at: 2026-10-05T16:08:26Z
completed_at: 2026-10-05T17:30:22Z
branch: claude/stock-photo-source
depends_on:
  - 2026-10-05-media-locate-subject-boxes
scope:
  - apps/api/app/config.py
  - apps/api/app/admin/service.py
  - apps/api/app/video_media/stock.py
  - apps/api/tests/test_video_media_stock.py
  - apps/api/tests/test_admin_readiness.py
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

- [x] `POST /video/media/stock/search {query, orientation, per_page}` returns candidates with
      photographer, page URL and licence; `POST /video/media/stock/fetch {slug, provider, id}`
      downloads the original into the media store and returns `{sha256, width, height, credit:
      {author, url, license, provider}}`. Not a `video_media_jobs` row (the kind CHECK stays
      image / clip / music).
- [x] Keys are server-only (`pexels_api_key`, `pixabay_api_key`), tested by the settings page's
      connection test, pinned to `api.pexels.com` and `pixabay.com`.
- [x] The provider shows on the settings page in the right category with five-locale labels.

## Steps

- [x] `config.py`, `admin/service.py` (`ProviderDefinition`, `CONNECTION_TESTED_PROVIDERS`),
      `OFFICIAL_PROVIDER_HOSTS`; the existing provider enumeration tests (find with
      `grep -rl CONNECTION_TESTED_PROVIDERS apps/api/tests apps/web/components` and add them to scope).
- [x] `video_media/stock.py` + tests with `httpx.MockTransport`; routes and schemas; `storage.py`
      accepts the fetched original.
- [x] `admin-settings-panel.tsx` category + `admin.json` ×5 labels + ownership; `ILLUSTRATED.md`.
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

### Done (2026-10-05, branch `claude/stock-photo-source`, on top of #1294)

- `stock.py` is one module for both vendors: `vendors()` lists the configured ones in a fixed
  order (Pexels, Pixabay) or the one asked for, 503 `video_media_stock_unavailable` when there
  is none; `search()` asks each vendor once and only fails when none answered (a vendor that
  failed beside one that answered is named in `problems`); `fetch()` makes the by-id call again
  rather than trusting a URL from the tool, takes the largest file (Pexels `src.original`;
  Pixabay `imageURL` → `fullHDURL` → `largeImageURL`, the first two only with full API access),
  checks the host with the existing `check_download` against `HOSTS` (`images.pexels.com`;
  `pixabay.com`, `cdn.pixabay.com`), streams into `MediaStore.put_stream(..., accept=IMAGE_TYPES)`
  under the name `stock-<vendor>-<id>`, and reads `width`/`height` from the stored bytes with
  Pillow (the vendor's numbers are not trusted; an unreadable file is unlinked again).
- Every answer carries `credit {provider, author, author_url, url, license, license_url, text}`
  with the vendor's own credit wording ("Photo by … on Pexels", "Image by … from Pixabay");
  `ILLUSTRATED.md §圖庫照片` holds the licence and API rules the sibling ticket must honour
  (credit in the description, no hotlinking, Pixabay results cached ≤ 24 h).
- Keys: `Settings.pexels_api_key`/`pixabay_api_key` plus `pexels_api_base_url`/
  `pixabay_api_base_url` pinned in `OFFICIAL_PROVIDER_HOSTS` and checked in
  `validate_deployment_security`'s `pinned_endpoints`; `apply_runtime_overrides` already drops a
  stored off-host URL for any pinned field (tested). Pixabay takes its key as a query
  parameter, so `_check`/`_get` never put a URL into an error; only the vendor's label and the
  HTTP status (Pixabay answers 400 to a bad key as well as to a bad parameter, said so).
- Admin: `stock_photos` card (`PROVIDER_DEFINITIONS`, `_configured`, `CONNECTION_TESTED_PROVIDERS`,
  `_test_provider` → `stock.probe()`: one real "Seoul skyline" search per configured vendor,
  per_page 1 / Pixabay's minimum 3, every vendor tried, one failure fails the test with the
  others' results beside it). Web: new category `video` (「影片素材」) in `providerCategories` +
  `providerTabs.categories.video` ×5, because the existing `content` tab is labelled "Hotspot
  content"; `secretLabels` + `providerSecrets.{pexels,pixabay}_api_key` ×5; the base URLs use
  non-localized `fieldMeta` labels like `minimax_api_base_url`. Ownership needed no change:
  `settingsOwner` already files secrets and unknown providers under the shared providers page.
- Routes: `POST /stock/search`, `POST /stock/fetch` on `media_router`; one shared per-hour
  bucket `video_media_stock` (`STOCK_CALLS_PER_HOUR` 150, under Pexels's 200/h); no meter, no
  job row; a fetch that stored a file runs `_prune_sometimes` like a job write. `GET /status`
  gains `stock: {pexels, pixabay}` and `limits.stock_per_page` (40). `_refused` takes
  `StockError`; `StorageRefused` from a fetch goes through `_storage_refused` as before.
- `storage.py`: `put_stream`'s second argument is now `name` (a job id or `stock-…`), guarded by
  `INCOMING_NAME` (422 `video_media_bad_name`), and `accept=` narrows the sniffed types
  (415 `video_media_unsupported_type` with the accepted extensions named).
- Scope: `apps/api/tests/test_admin_readiness.py` added, as the Steps said to, for the
  enumeration test (`CONNECTION_TESTED_PROVIDERS | LOCAL_ONLY_PROVIDERS == PROVIDER_DEFINITIONS`
  already covers the new card; a stock-specific `card_state` test was added beside it).
- Not measured live: this container has no Pexels or Pixabay key, so the field names follow the
  vendors' public API documentation and the first real call should check what `ILLUSTRATED.md`
  §沒實測的事 lists. Pixabay has no `square` orientation filter, so `square` is sent to Pexels
  only and Pixabay's candidates are returned unfiltered (their sizes are in the answer).
- Not in scope, noticed: `docs/videos/DRAMA.md` §端點 does not list the stock routes
  (`ILLUSTRATED.md` does); `apps/api/tests/test_video_media_api.py`'s 401 route list does not
  name them (`test_video_media_stock.py` checks both routes); `.env.example` does not mention
  `PEXELS_API_KEY`/`PIXABAY_API_KEY`; `tools/video/media/client.mjs` has no stock calls yet
  (`2026-10-05-stock-photo-slides-and-attribution`).
- Receipt: the five `admin.json` files are bound; the increment is the independent reviewer's.
