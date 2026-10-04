---
id: 2026-10-04-minimax-h3-adapter-v2-shape
title: MiniMax H3 adapter sends the v1 request shape with a first frame and a subject reference, which the official v2 API forbids
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-04T15:44:58Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_media/providers/minimax.py
  - apps/api/app/video_media/catalog.py
  - apps/api/tests/test_video_media_providers.py
---

# MiniMax H3 adapter sends the v1 request shape with a first frame and a subject reference, which the official v2 API forbids

## Why

`apps/api/app/video_media/providers/minimax.py` posts model `MiniMax-H3` to `<base>/video_generation`
with the v1 body (`prompt`, `first_frame_image`, optional `last_frame_image`, `prompt_optimizer`,
`subject_reference`). The official docs (platform.minimax.io, read 2026-10-04) serve H3 only on
`/v2/video_generation` with a `content[]` array, and make image-to-video (first/last frame) and
reference-to-video (reference images, video, audio) mutually exclusive; the v1 model list has no
H3. The server H3 route has never made a clip, so it may fail at submission or silently drop the
references. `catalog.py` also lists H3 durations 4–10 while the official range is 4–15.

## Definition of done

- [ ] One dry or paid check shows what the configured endpoint (`api.minimaxi.com` China domain by default, `api.minimax.io` international) accepts for H3.
- [ ] The adapter sends the documented shape for H3 and never mixes a first frame with references; tests pin the body.
- [ ] `catalog.py` durations match the official range, or the reason they do not is written next to them.

## Steps

- [ ] Read the v2 create, regeneration and Context-IR docs; decide whether the China domain matches.
- [ ] Change the adapter and `apps/api/tests/test_video_media_providers.py`.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_media_providers.py -q
```

## Notes

- Found by the official-docs research for `2026-10-04-animation-preproduction-skill`; the official notes are summarized in `.agents/skills/animation-preproduction/references/route-decisions.md`.
- Spending on a check needs the owner's approval.
