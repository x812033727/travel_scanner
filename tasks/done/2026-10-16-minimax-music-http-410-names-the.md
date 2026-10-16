---
id: 2026-10-16-minimax-music-http-410-names-the
title: MiniMax music HTTP 410 names the 2026-08-20 rule and is the owner's to fix
status: done
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-10-16T00:34:20Z
created_at: 2026-10-16T00:33:26Z
completed_at: 2026-10-16T01:02:40Z
branch:
depends_on: []
scope:
  - apps/api/app/video_media/providers/minimax.py
  - apps/api/tests/test_video_media_providers.py
  - docs/videos/DRAMA.md
---

# MiniMax music HTTP 410 names the 2026-08-20 rule and is the owner's to fix

## Why

On 2026-10-16 production MiniMax answered HTTP 410 for both music-3.0 and music-2.6. The
job failed as `video_media_upstream_failed` with only "MiniMax answered HTTP 410", which
reads like a vendor outage a retake might fix. A 410 from the music endpoint is the
documented shape of the paid music API being closed (since 2026-08-20) to accounts that
never bought music, so only the owner can fix it, by switching provider.

`MiniMaxMusic.submit` named the rule only for `raise_for_status`'s `key` (401/403) and
`invalid` (404); a 410 falls to its generic `failed`.

## Definition of done

- [x] A 410 from `/music_generation` fails the job as `key`
      (`video_media_upstream_rejected_key`) and the message names the 2026-08-20 rule.
- [x] Other music statuses keep their kinds (429 busy, 5xx failed, 400 blocked).
- [x] DRAMA.md 背景音樂 row records the 2026-10-16 observation.

## Steps

- [x] `MiniMaxMusic.submit` turns a 410 into a `key` error with the rule.
- [x] Test case next to the 401/403/404 music cases.
- [x] DRAMA.md row.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run mypy tests && uv run pytest tests/test_video_media_providers.py
```

## Notes

The shared `raise_for_status` is left alone: a 410 elsewhere (an expired download, say)
is not an account problem, so only the music endpoint reads it as one.
