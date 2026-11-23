---
id: 2026-11-13-minimax-h3-image-as-a-site
title: MiniMax H3-Image as a site image model, tested against image-01 for curio and so-thats-why
status: in-progress
priority: P2
area: api
owner: claude-opus-session-41c1d91a
claimed_at: 2026-11-13T06:29:37Z
created_at: 2026-11-13T06:29:31Z
completed_at:
branch: claude/h3-image-test
depends_on: []
scope:
  - apps/api/app/video_media/providers/minimax.py
  - apps/api/app/video_media/catalog.py
  - apps/api/tests/test_video_media_providers.py
  - apps/api/tests/test_video_media_catalog.py
  - tools/video/media/prompt-budget.mjs
---

# MiniMax H3-Image as a site image model, tested against image-01 for curio and so-thats-why

## Why

MiniMax released H3-Image on 2026-11-10. The owner (2026-11-13) wants to try it on the site's
own MiniMax key (an M Plan subscription key, `minimax_api_*`) as a replacement for image-01 in
奇聞檔案局 (curio-*) and 原來如此事務所 (so-thats-why). The site only draws with catalog models,
and H3-Image has its own API (`/v1/images/generations`, `/v1/images/edits`), so it needs an
adapter before a single picture can be tried.

## Definition of done

- [x] `MiniMax-H3-Image` is a catalog image model on the minimax vendor (1K and 2K, up to 4
      references, no style plate) and the MiniMax image adapter sends it to the H3 endpoints.
- [ ] Deployed, then a small comparison batch (owner approves the spend; about US$0.02–0.03 a
      picture) drawn with the same prompts as an existing curio and so-thats-why episode.
- [ ] Recorded here: whether the M Plan key may call it at all (402 `2068` means the plan tier
      lacks the model), what it cost, and the owner's verdict.
- [ ] Only if the owner chooses it: switching the two series (cute-mystery and so-thats-why
      checks still require image-01 in `stories.py`, `series.py`, `schemas.py`, `story.mjs`,
      `plan.mjs`, `so-thats-why/catalog.mjs`) is a separate task.

## How to verify

```bash
cd apps/api && uv run pytest -q tests/test_video_media_providers.py -k h3_image
node --test tools/video/media/media.test.mjs
```

## Notes

- API pages read 2026-11-13: image-generation-h3-generations / -h3-edits. No seed and no
  negative prompt; generations takes `disable_prompt_enhanced` (sent true, like image-01's
  `prompt_optimizer: false`); edits always rewrites the prompt. Errors are HTTP statuses with
  `(code)` at the end of an OpenAI-style message, like the v2 video API, so `raise_for_v2` maps
  them. Per-picture failures come back as HTTP 200 with `data[0].error`.
- Open-weights licence excludes the US, EU, UK and Korea; Taiwan is inside the territory. The
  hosted API is under MiniMax's service terms (not read).
