---
id: 2026-10-05-minimax-h3-reference-route-a-clip
title: MiniMax H3 reference route: a clip job may leave the first frame out, and the catalog counts the reference images the endpoint took
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-05T17:56:47Z
completed_at:
branch:
depends_on:
  - 2026-10-05-minimax-h3-v2-live-check
  - 2026-10-05-h3-reference-to-video-v2
scope:
  - apps/api/app/video_media/schemas.py
  - apps/api/app/video_media/jobs.py
  - apps/api/app/video_media/catalog.py
  - apps/api/tests/test_video_media_jobs.py
  - apps/api/tests/test_video_media_api.py
  - apps/api/tests/test_video_media_providers.py
  - tools/video/media/clips.mjs
  - tools/video/media/clips.test.mjs
---

# MiniMax H3 reference route: a clip job may leave the first frame out, and the catalog counts the reference images the endpoint took

## Why

`2026-10-05-h3-reference-to-video-v2` taught `apps/api/app/video_media/providers/minimax.py`
the documented v2 reference-to-video body (the text and up to nine `reference_image` items in
`content[]`, plus `ratio`; `V2_MAX_REFERENCE_IMAGES`), and it refuses a frame beside a
reference image before the paid call, since the v2 page makes the two shapes mutually
exclusive. Nothing on the site can send that body yet: `ClipJobIn.first_frame`
(`apps/api/app/video_media/schemas.py`) is required, so every clip job carries a first frame;
`jobs._request_fields` refuses a reference for a model whose catalog `reference_images` is 0;
and `tools/video/media/clips.mjs` sends the character sheets whenever that number is not 0.
Flipping the catalog to 9 today would make the clips tool send sheets beside every H3 first
frame, which the adapter then refuses: the H3 route would stop making clips, and
`tests/test_video_media_jobs.py::test_h3_refuses_a_reference_its_v2_request_could_never_carry`
pins the present behaviour. So the catalog keeps 0, and `tests/test_video_media_providers.py`
pins the coupling (`ClipJobIn.first_frame` required while H3 is at 0). This ticket is the other
half: a clip job that starts from reference images instead of a keyframe, and the catalog
number that follows from the live check.

## Definition of done

- [ ] A `ClipJobIn` for `MiniMax-H3` with character references and no `first_frame` is
      accepted by the clip job endpoint and reaches the adapter as a reference-to-video
      request; one with both is refused 422 at the jobs layer before a row or a budget
      reservation exists; every other clip model still requires its first frame.
- [ ] `catalog.py` gives `MiniMax-H3` the number of reference images the live check saw the
      endpoint accept (the documented maximum is 9, `V2_MAX_REFERENCE_IMAGES`), the clips tool
      sends sheets only on the reference route and never beside a first frame, and the provider
      test that pins the coupling is rewritten with it.
- [ ] One paid comparison (owner's approval): the same shot with and without references, the
      judge's identity score for each, recorded here.

## Steps

- [ ] `schemas.py`: `first_frame` optional on `ClipJobIn`, with a validator that a clip has a
      first frame or references, never neither; `jobs.py`: the reference route for a v2 model,
      the refusal of both, the per-model count.
- [ ] `clips.mjs`: the shot-level choice of the reference route (the shot field is bound,
      `SHOT_KEYS`; `clips.mjs` was contested on 2026-10-05, run `who-is-on-it.mjs` first).
- [ ] `catalog.py` and the tests in scope.
- [ ] The paid comparison, after the live check and only with the owner's yes.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_media_providers.py tests/test_video_media_jobs.py tests/test_video_media_api.py -q
npm run test:tools
```

## Notes

- Split from `2026-10-05-h3-reference-to-video-v2`, whose Notes hold the official pages read on
  2026-10-05 and the request shape. The live check ticket as written records
  `usage.input_image_count` for one image-to-video clip only; the reference count needs one
  reference-to-video call, which this ticket asks for with the owner's approval.
- The adapter sends every reference image in the order given, whatever its role, since the
  text names them by number; the tool decides which sheets go and writes the official
  six-section Ref2VA prompt (`.agents/skills/animation-camera/references/model-misreads.md`
  §六 names the format).
