---
id: 2026-10-04-minimax-h3-adapter-v2-shape
title: MiniMax H3 adapter sends the v1 request shape with a first frame and a subject reference, which the official v2 API forbids
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-minimax-h3-v2
claimed_at: 2026-10-05T01:18:44Z
created_at: 2026-10-04T15:44:58Z
completed_at:
branch: claude/minimax-h3-v2
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
- [x] The adapter sends the documented shape for H3 and never mixes a first frame with references; tests pin the body.
- [x] `catalog.py` durations match the official range, or the reason they do not is written next to them.

## Steps

- [x] Read the v2 create, regeneration and Context-IR docs; decide whether the China domain matches.
- [x] Change the adapter and `apps/api/tests/test_video_media_providers.py`.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_media_providers.py -q
```

## Notes

- Found by the official-docs research for `2026-10-04-animation-preproduction-skill`; the official notes are summarized in `.agents/skills/animation-preproduction/references/route-decisions.md`.
- Spending on a check needs the owner's approval.

### 2026-10-05: what was done (claude-opus-5-5-minimax-h3-v2)

- **Split.** The first Definition-of-done item (a dry or paid call against the configured
  endpoint) needs the site's real key on the production host and the owner's approval to
  spend, so it is not ticked here and moved, with the host question below, to
  `2026-10-05-minimax-h3-v2-live-check`. Nothing was sent to MiniMax's API from this ticket.
- **Docs read on 2026-10-05** (curl with the editorial User-Agent, no key):
  - create: https://platform.minimax.io/docs/api-reference/video-generation-v2-create (`POST /v2/video_generation`)
  - query: https://platform.minimax.io/docs/api-reference/video-generation-v2-query (`GET /v2/query/video_generation/{task_id}`)
  - regeneration: https://platform.minimax.io/docs/api-reference/video-generation-v2-regeneration (`POST /v2/video_regeneration`, an H3 768P clip to 2K; by `source_task_id` needs a whitelist, otherwise resend the full `content` plus one `role=base_video` item)
  - Context-IR: https://platform.minimax.io/docs/api-reference/video-generation-v2-h3-context-ir (`POST /v2/h3_context_ir`, returns only an enhanced prompt in `content.prompt`, no video)
  - guide: https://platform.minimax.io/docs/guides/video-generation (polls every 10 s; `content.url` is the video, no file-id exchange)
  - v1: https://platform.minimax.io/docs/api-reference/video-generation-i2v (models `MiniMax-Hailuo-2.3`, `-2.3-Fast`, `-02`, `I2V-01-Director`; no H3)
  - China: https://platform.minimaxi.com/docs/api-reference/video-generation-v2-create and `-v2-query` redirect to `platform.minimax.cn`; same paths, same body, same rules. Their OpenAPI `servers` entry is `https://api.minimax.cn`, not `api.minimaxi.com` (the site's default, `app/config.py`). Whether `api.minimaxi.com` still answers `/v2` needs the live call.
- **The v2 request shape** (required: `model`, `content`, `resolution`, `duration`):
  `{"model": "MiniMax-H3", "content": [{"type": "text", "text": …}, {"type": "image_url", "image_url": {"url": …}, "role": "first_frame"}, {… "role": "last_frame"}], "resolution": "768P"|"2K", "duration": 4…15}`.
  Exactly one non-empty `text` (≤ 7,000 characters). `image_url.url` is a public URL, `mm_file://{file_id}` or `data:image/<format>;base64,…` (lower-case format). Image-to-video (`first_frame`, `last_frame`; a last frame pairs with a first) and reference-to-video (`reference_image` ≤ 9, `reference_video` ≤ 3, `reference_audio` ≤ 3) are mutually exclusive. `ratio` is optional and ignored in image-to-video (always `adaptive`); `extra.prompt_expansion_mode` is for H3-Max only; `callback_url` optional. Body ≤ 64 MB; images ≤ 30 MB, 256–5,760 px a side, ratio 0.4–2.5. The answer is `{"task_id": "…"}` (a string). The query answers `{"task": {"status": queued|running|succeeded|failed|cancelled, "content": {"url"}, "error": {"code", "message"}, "usage": {…}}}` for 7 days. Errors are real HTTP statuses (400, 401, 402, 422, 429, 500, 529) with an OpenAI-style body whose `error.message` ends in MiniMax's own code, e.g. `(2013)`.
- **What the adapter does now** (`apps/api/app/video_media/providers/minimax.py`): `MiniMax-H3` (the only name in `V2_VIDEO_MODELS`) posts that body to `<host>/v2/video_generation`, the host being the configured base without its `/v1`. It sends the prompt (with the `Avoid:` text, as v1 did), the first frame and an optional last frame, and nothing else: no character sheets (every clip has a first frame), no `ratio`, no `prompt_optimizer`. A missing resolution is refused before the network. The task id is stored as `v2:<id>` (a number is accepted, since the task is already paid for), and `poll` reads that prefix to ask `/v2/query/video_generation/<id>`. A v2 refusal keeps only the code: 2013 or a bare 400 is `invalid`, 1004/1008/2049 or 402 is `key`, 1026/1027 or 422 is `blocked`, 429/529 is `busy`; a failed task with 1026/1027 is `blocked` too, so the tools may retake.
- **Every other model keeps v1 byte for byte.** Before changing the adapter, the first commit pinned the v1 request for Hailuo 2.3, Hailuo 02 and I2V-01-Director against the unchanged code: URL, request bytes (httpx's own encoder, so key order counts), the task id as sent, and the query and `files/retrieve` URLs. Those tests pass unchanged after the change.
- **Durations stay 4–10**, with the reason next to them in `catalog.py`: the drama tools never ask for more than 10 seconds (`MAX_CLIP_SECONDS`), the estimator mirrors the catalog (`tools/animation-production.test.mjs` compares them, and five skill pages say "catalog 4–10"), and 11–15 s would raise one 2K clip to US$1.95 on a request never accepted live. The admin note now says so, and that H3 gets no reference images.
- No H3-Max: it is v2-only as well, but it is not in the catalog; adding it means a price and a model decision.
