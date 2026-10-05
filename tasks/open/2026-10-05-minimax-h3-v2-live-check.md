---
id: 2026-10-05-minimax-h3-v2-live-check
title: Live-check the MiniMax H3 v2 request on the configured endpoint before an H3 clip is bought
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-05T01:52:03Z
completed_at:
branch:
depends_on:
  - 2026-10-04-minimax-h3-adapter-v2-shape
scope:
  - apps/api/app/video_media/providers/minimax.py
  - apps/api/tests/test_video_media_providers.py
---

# Live-check the MiniMax H3 v2 request on the configured endpoint before an H3 clip is bought

## Why

Split from `2026-10-04-minimax-h3-adapter-v2-shape`. That ticket moved `MiniMax-H3` in
`apps/api/app/video_media/providers/minimax.py` from the v1 request (which has no H3 in its
model list) to the documented v2 request: `POST <host>/v2/video_generation` with a `content[]`
array (text, `first_frame`, optional `last_frame`, never a reference beside a frame), polled at
`GET <host>/v2/query/video_generation/{task_id}`. The shape comes from MiniMax's official pages
read on 2026-10-05 and is pinned by tests, but nothing has ever been sent: no H3 clip has been
made by the server route, and the tests prove only what we send, not what MiniMax accepts.

Three things only a real call can settle:

- **The host.** The site's default base is `https://api.minimaxi.com/v1` (`app/config.py`), and
  the allowlist takes `api.minimaxi.com` and `api.minimax.io`. On 2026-10-05
  `platform.minimaxi.com` redirected to `platform.minimax.cn`, whose v2 pages name
  `https://api.minimax.cn` as the server. Whether `api.minimaxi.com` still answers `/v2` is
  unknown. If it does not, the default and `OFFICIAL_PROVIDER_HOSTS` need `api.minimax.cn`
  (then widen this ticket's scope to `apps/api/app/config.py` first).
- **The account.** The create page says H3 needs the Pay-as-you-go API; whether the site's key
  has it is unknown.
- **The body.** Whether a data-URI first frame, the upper-case `768P`/`2K` and no `ratio` are
  accepted as documented, and whether H3 rewrites the prompt (v2 has no `prompt_optimizer`; only
  H3-Max takes `extra.prompt_expansion_mode`).

Spending on any of this needs the owner's approval, and the key lives in the site's settings on
the production host, so this is not for an agent to run alone.

## Definition of done

- [ ] One dry call (no generation) shows whether the configured host serves `POST /v2/video_generation` for `MiniMax-H3` with the site's key: the HTTP status and the code at the end of the error message are recorded here.
- [ ] With the owner's approval, one paid H3 clip (768P, 4 seconds: US$0.32 at the official 768P price; the site's meter books US$0.52, since it prices every H3 second at the 2K rate) goes through the site's normal clip job and is stored, or the exact refusal is recorded here and the adapter is fixed to match.
- [ ] If the configured host does not serve v2, the host question is settled (default and allowlist changed, or the owner sets `api.minimax.io`), with the reason written here.

## Steps

- [ ] Ask the owner for approval and for the host session (skill `prod-host-ops`); no key or host detail goes into this file.
- [ ] Dry call: post a body with an empty `content` (`{"model":"MiniMax-H3","content":[],"resolution":"768P","duration":4}`). The documented answer is HTTP 400 with code 2013 ("content must include a non-empty text item"), which proves path, key and model without generating anything. A 404 means the host has no v2; 401 or code 1004 the key; 402 or 1008 the balance or plan.
- [ ] Paid clip, only after the owner says yes: set the clip model to `MiniMax-H3` at 768p and run one 4-second clip job from an approved keyframe; record the task id format, the query answers seen (`queued`/`running`/`succeeded`), the download host, `usage.input_image_count` (1 when only the first frame went), and whether the clip follows the prompt as written.
- [ ] Fix `minimax.py` and its tests for anything that differed, and record the answers in Notes.

## How to verify

```bash
cd apps/api && PYTHONUTF8=1 uv run pytest tests/test_video_media_providers.py -q
```

The live part is proven only by the recorded answers above and by the stored clip's job row
(`status` ready, `vendor_ref` starting with `v2:`).

## Notes

- Official pages (read 2026-10-05): https://platform.minimax.io/docs/api-reference/video-generation-v2-create, https://platform.minimax.io/docs/api-reference/video-generation-v2-query, https://platform.minimax.io/docs/guides/video-generation; China: https://platform.minimaxi.com/docs/api-reference/video-generation-v2-create (redirects to platform.minimax.cn, server `https://api.minimax.cn`). The full request shape is in the Notes of `tasks/done/2026-10-04-minimax-h3-adapter-v2-shape.md`.
- The catalog keeps H3 at 4 to 10 seconds on purpose (comment in `apps/api/app/video_media/catalog.py`). Opening 11 to 15 after this check is the owner's call and a separate ticket: it also touches `.agents/skills/animation-production/scripts/episode_estimate.mjs` (pinned equal by `tools/animation-production.test.mjs`) and the skill pages that say "catalog 4–10".
- An H3 job still `submitted` from before the change carries a v1 task id without the `v2:` prefix and keeps polling v1, as it did; the original ticket says the server route never made an H3 clip.
