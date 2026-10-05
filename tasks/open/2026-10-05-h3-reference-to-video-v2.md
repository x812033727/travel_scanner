---
id: 2026-10-05-h3-reference-to-video-v2
title: MiniMax H3 reference-to-video in the v2 adapter: character sheets reach the clip
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-05T16:08:27Z
completed_at:
branch:
depends_on:
  - 2026-10-05-minimax-h3-v2-live-check
scope:
  - apps/api/app/video_media/providers/minimax.py
  - apps/api/app/video_media/catalog.py
  - apps/api/tests/test_video_media_providers.py
  - docs/videos/DRAMA.md
---

# MiniMax H3 reference-to-video in the v2 adapter: character sheets reach the clip

## Why

Every clip is image-to-video from the keyframe alone: Veo Lite and MiniMax H3 take zero
references, so a character's identity rides on the first frame and the 2026-10-03 trial lost
hands and props in three of four takes. MiniMax H3's official API supports reference-to-video
(images, videos and audio named as "Image 1…"); the v2 adapter never sends references
(`2026-10-04-minimax-h3-adapter-v2-shape` corrected the catalog's promise instead). Once the
live check settles the endpoint, the references can reach the clip.

## Definition of done

- [ ] A `ClipJobIn` for `MiniMax-H3` with character references and no `first_frame` becomes
      the documented v2 reference-to-video body; one with both is refused 422
      (`video_media_invalid`) rather than silently dropping either.
- [ ] The catalog's `reference_images` for H3 is the number the live check recorded; tests pin
      both bodies.
- [ ] One paid comparison (owner's approval): the same shot with and without references, the
      judge's identity score for each, recorded here.

## Steps

- [ ] `providers/minimax.py` body builder + tests; `catalog.py`; `DRAMA.md` 供應商表.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_media_providers.py -q
```

## Notes

- No bound file. The tool-side choice (a shot without a keyframe taking the reference route)
  is deferred: it needs a shot field (`SHOT_KEYS`, bound) and `clips.mjs` (contested).
