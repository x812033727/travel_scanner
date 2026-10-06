---
id: 2026-10-05-h3-reference-to-video-v2
title: MiniMax H3 reference-to-video in the v2 adapter: character sheets reach the clip
status: done
priority: P3
area: api
owner: claude-fable-5-1-h3
claimed_at: 2026-10-05T17:51:09Z
created_at: 2026-10-05T16:08:27Z
completed_at: 2026-10-05T18:11:14Z
branch: claude/h3-reference-to-video
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

- [x] A `ClipJobIn` for `MiniMax-H3` with character references and no `first_frame` becomes
      the documented v2 reference-to-video body; one with both is refused 422
      (`video_media_invalid`) rather than silently dropping either.
      (Done at the adapter, on the `MediaRequest` a job becomes: `providers/minimax.py` builds
      the reference-to-video body and refuses a frame beside a reference image before the paid
      call, kind `invalid`, which the jobs layer records as `video_media_upstream_invalid`. A
      `ClipJobIn` itself cannot leave `first_frame` out yet, and the jobs layer refuses the
      both-case first, unspent, as `video_media_model_not_allowed`; that half is
      `2026-10-05-minimax-h3-reference-route-a-clip`.)
- [ ] The catalog's `reference_images` for H3 is the number the live check recorded; tests pin
      both bodies. (Awaits the live check ticket. The tests pin both bodies; the catalog stays
      0 on purpose while `ClipJobIn.first_frame` is required, with the documented maximum
      recorded as `V2_MAX_REFERENCE_IMAGES = 9` in the adapter; the Notes say why, and the
      number moves with `2026-10-05-minimax-h3-reference-route-a-clip`.)
- [ ] One paid comparison (owner's approval): the same shot with and without references, the
      judge's identity score for each, recorded here. (Needs the owner's approval, the live
      check and a clip job that can take the reference route: carried by
      `2026-10-05-minimax-h3-reference-route-a-clip`.)

## Steps

- [x] `providers/minimax.py` body builder + tests; `catalog.py`; `DRAMA.md` 供應商表.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_media_providers.py -q
```

## Notes

- No bound file. The tool-side choice (a shot without a keyframe taking the reference route)
  is deferred: it needs a shot field (`SHOT_KEYS`, bound) and `clips.mjs` (contested).

### 2026-10-05: what was done (claude-fable-5-1-h3)

- **Claimed with `--force`** over the unfinished dependency `2026-10-05-minimax-h3-v2-live-check`:
  that ticket needs the site's real MiniMax key on the production host and the owner's
  approval to spend, neither of which this session had. Nothing was sent to MiniMax; every test
  runs on `httpx.MockTransport`.
- **Official pages read on 2026-10-05:**
  - create: https://platform.minimax.io/docs/api-reference/video-generation-v2-create. A
    `content[]` item is `{"type": "text"|"image_url"|"video_url"|"audio_url", …, "role": …}` with
    roles `first_frame`, `last_frame`, `reference_image`, `reference_video`, `reference_audio`;
    "first frame ≤ 1, last frame ≤ 1, reference images ≤ 9", reference videos ≤ 3, audio ≤ 3;
    "Image-to-video and reference-to-video are mutually exclusive: if any `reference_image` /
    `reference_video` / `reference_audio` role appears in content, then `first_frame` /
    `last_frame` must not appear (and vice versa); the two cannot be mixed." One non-empty text
    item, ≤ 7,000 characters. `image_url.url` is a public URL, `mm_file://{file_id}` or
    `data:image/<format>;base64,…` (format lower-case), the same for a reference image as for
    a frame; images ≤ 30 MB, 256–5,760 px a side, w/h 0.4–2.5. `ratio` is optional, default
    `adaptive`, concrete values `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16`; in image-to-video
    it is always adaptive to the input image. MiniMax-H3: `768P`/`2K`, 4–15 s; H3-Max:
    `480P`/`768P`, 5–15 s. The page says nothing about how the text names the pictures.
  - guide: https://platform.minimax.io/docs/guides/video-generation. Its reference-to-video
    example sends `{"type": "image_url", "image_url": {"url": …}, "role": "reference_image"}`
    items with a text saying "The character's appearance follows reference images 1 and 2";
    mixed reference input "capped at 12 files in total"; poll every 10 s; the video is
    `task.content.url`.
  - China: https://platform.minimax.cn/docs/api-reference/video-generation-v2-create (the
    minimaxi.com address redirects there): server `https://api.minimax.cn`, the same roles,
    counts, ratios and models, and the rule verbatim: 「图生视频与多模态参考生视频互斥：content
    中出现 reference_image / reference_video / reference_audio 任一 role，就不能再出现
    first_frame / last_frame（反之亦然），二者不可混用。」
  - prompt format: https://huggingface.co/MiniMaxAI/MiniMax-H3/raw/main/docs/VIDEO_PROMPT_WRITING_GUIDE_ref_en.md
    (the official Ref2VA guide the model-misreads §六 names): six sections
    `subject_definitions`, `summary`, `retention_analysis`, `detailed_description`,
    `overall_soundscape`, `non_diegetic_music`; the pictures are `<Picture N>` and a subject is
    bound to one in `subject_definitions`; no maximum stated. Writing that prompt is the
    tool's job; the adapter sends the text as written.
- **What the adapter does now** (`apps/api/app/video_media/providers/minimax.py`): a
  `MediaRequest` for `MiniMax-H3` with reference images and no frame posts
  `{"model", "content": [text, reference_image × n], "resolution", "duration", "ratio"}` to
  `<host>/v2/video_generation`, every reference image in the order given, whatever its role
  (the text numbers them), `ratio` = the request's aspect (the drama's `16:9`/`9:16`; a value
  the page does not list is refused). A frame beside a reference image, a last frame alone,
  nothing to start from, more than `V2_MAX_REFERENCE_IMAGES` (9) pictures or a missing
  resolution are each refused with a fixed message, kind `invalid`, before anything is sent.
  Image-to-video is byte for byte what it was, and every other model keeps v1 unchanged (its
  "a clip needs its first frame" refusal included). `v2_image` builds one picture item.
- **Why the catalog's `reference_images` stays 0.** The ticket (and the brief for this
  session) wanted the documented maximum written there. That number is read as "how many
  sheets may ride beside the first frame": `jobs._request_fields` refuses references when it
  is 0, and `tools/video/media/clips.mjs` sends the sheets whenever it is not. Every clip job
  has a first frame (`ClipJobIn.first_frame` is required, `schemas.py`, outside this scope),
  so 9 would make the clips tool send sheets beside every H3 first frame, the adapter would
  refuse each (correctly: the page forbids the mix), no H3 clip could be made, and
  `tests/test_video_media_jobs.py::test_h3_refuses_a_reference_its_v2_request_could_never_carry`
  (outside this scope) would fail. So the documented maximum lives in the adapter as
  `V2_MAX_REFERENCE_IMAGES = 9`, the catalog comment and the settings-tab note say the
  adapter can build the request, and
  `test_the_catalog_keeps_h3_at_zero_references_while_every_clip_job_has_a_first_frame` pins
  the coupling: it fails, naming the constant to copy in, as soon as `first_frame` becomes
  optional. Flipping the number, the schema, the jobs route and the tool side are
  `2026-10-05-minimax-h3-reference-route-a-clip` (depends on this ticket and the live check).
- **Tests** (`apps/api/tests/test_video_media_providers.py`): `_h3_request` is an H3
  image-to-video request without sheets, since sheets beside a frame are now refused; the
  i2v body test no longer carries sheets it expects dropped; a reference-to-video test pins
  the body and the bytes sent, for `16:9` and `9:16`; nine pictures go, ten are refused; a
  table of eight refusals proves nothing reaches the endpoint; the catalog test pins the
  coupling above. 144 tests pass across the four video media suites.
- **Noticed, not fixed:** the live check ticket's DoD records `usage.input_image_count` for one
  image-to-video clip only, so "the number the live check recorded" needs one
  reference-to-video call too; the follow-up ticket asks for it. `docs/videos/DRAMA.md` still
  heads its provider table "2026-09-26 查官方頁"; the H3 cell now carries its own date.
