---
id: 2026-09-24-store-news-images-without-s3-on
title: Store news images without S3 on hosts that have none
status: done
priority: P1
area: api
owner: claude-opus-5.5
claimed_at: 2026-09-24T01:56:35Z
created_at: 2026-09-24T01:56:27Z
completed_at: 2026-09-24T01:59:26Z
branch: claude/news-assets-without-s3
depends_on: []
scope:
  - apps/api/app/news_automation/assets.py
  - apps/api/app/news_automation/models.py
  - apps/api/app/news_automation/jobs.py
  - apps/api/migrations/versions/0085_news_asset_inline_content.py
  - apps/api/tests/test_news_assets_storage.py
  - docs/news-automation.md
---

# Store news images without S3 on hosts that have none

## Why

After the hardening in #703 was deployed, the news worker's log showed the daily
retention job failing with `community_storage_unavailable`: the production host has no
S3 bucket configured. News images are written to that same bucket, and the image step
runs after every model stage, so each candidate that passed the evidence gate would
have failed there after spending about ten MiniMax calls, and RQ would have retried it
twice more. Testing the image step without mocks then showed it could never succeed
anyway: `render_brand_raster` draws seven inset rings, and on the 1200x630 social card
the later rings invert, which PIL rejects with `ValueError`.

## Definition of done

- [x] Without object storage, a candidate's images are kept in its `news_assets` rows and
      served from there; with S3 configured nothing changes.
- [x] The social card renders; the 1600x900 hero is drawn exactly as before.
- [x] The retention job no longer needs S3 and clears row-held images of old unpublished
      candidates.

## Steps

- [x] Migration 0085 adds a nullable `news_assets.content` (bytea).
- [x] `_put` returns the bytes for the row when `storage()` is unavailable;
      `public_asset` serves the row first.
- [x] Stop the ring loop once a ring no longer fits.
- [x] Retention builds the S3 client only for S3-held assets.
- [x] Tests without mocks for the image step, both storage paths and retention.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_assets_storage.py tests/test_news_admin.py tests/test_news_pipeline.py -q
```

## Notes

- The pipeline test in #703 mocked `ensure_assets`, which is how the social-card crash
  survived; `test_news_assets_storage.py` runs the real renderer.
- The owner asked for the scanner to be switched on (MiniMax writer and checker, Jev
  review) after this deploys.
