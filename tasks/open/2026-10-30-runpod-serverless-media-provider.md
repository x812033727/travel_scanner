---
id: 2026-10-30-runpod-serverless-media-provider
title: RunPod Serverless as a server media provider so the worker buys H3 clips itself
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-30T00:37:24Z
completed_at:
branch:
depends_on:
  - 2026-10-30-runpod-pod-broker
  - 2026-10-30-runpod-h3-image-and-runner
  - 2026-10-30-runpod-canvas-and-import
scope:
  - apps/api/app/video_media/providers/runpod.py
  - apps/api/app/video_media/providers/__init__.py
  - apps/api/app/video_media/catalog.py
  - apps/api/app/video_media/jobs.py
  - apps/api/app/video_media/meter.py
  - apps/api/app/video_automation
  - apps/api/migrations/versions/0145_video_runpod_clip_provider.py
  - apps/api/tests/test_video_media_runpod.py
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings-drama.tsx
---

# RunPod Serverless as a server media provider so the worker buys H3 clips itself

## Why

Phase one still needs an agent session to drive the pod. For hands-off drama production the host
worker should buy RunPod H3 clips the same way it buys Gemini or MiniMax clips: through the API's
poll-driven media jobs.

## Definition of done

- [ ] `providers/runpod.py` implements `MediaProvider` (submit → RunPod Serverless `/run`, poll →
      `/status`, fetch the output) using `runpod_serverless_endpoint_id`.
- [ ] `runpod` added to `MediaVendor`, `MEDIA_VENDORS`, `provider_for`, the catalog, `meter.py`
      (USD per GPU-second) and `OFFICIAL_PROVIDER_HOSTS` (`api.runpod.ai`).
- [ ] Migration 0145 widens `ck_video_drama_providers` so `clip_provider` may be `runpod`;
      `MEDIA_PROVIDERS` in `admin-video-settings.tsx` and the drama tab offer it, and
      `drama_problems` refuses it while the RunPod card is incomplete.
- [ ] Existing monthly clip-seconds and per-video USD caps apply unchanged.

## Steps

- [ ] Serverless handler image (same workflows as the pod image).
- [ ] Provider, catalog, meter, migration, settings UI.
- [ ] Tests with a fake Serverless API.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_video_media_runpod.py
npm run lint:web && npm run typecheck:web && npm run test:web
```

## Notes

- Start only after the pod pilot has stable numbers (phase one).
- Check the migration number against `main` when claiming; 0145 assumes the broker took 0144.
