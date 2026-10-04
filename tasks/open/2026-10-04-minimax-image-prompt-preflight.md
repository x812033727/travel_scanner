---
id: 2026-10-04-minimax-image-prompt-preflight
title: Validate MiniMax image prompt length before dispatch and distinguish invalid parameters
status: in-progress
priority: P1
area: api
owner: codex-video-stall-followthrough
claimed_at: 2026-10-04T11:01:44Z
created_at: 2026-10-04T10:55:59Z
completed_at:
branch: codex/video-stall-followthrough-20261004
depends_on: []
scope:
  - apps/api/app/video_media/providers/minimax.py
  - apps/api/tests/test_video_media_providers.py
---

# Validate MiniMax image prompt length before dispatch and distinguish invalid parameters

## Why

MiniMax image-01 joins the positive and avoidance prompts, exceeding its vendor
limit even when the positive prompt alone fits. Live recovery produced three
settled zero-cost parameter rejections. Error code 2013 was incorrectly classified
as content rejection, allowing the keyframe tool to buy another seed for the same
deterministic error. Validate the exact joined body before network dispatch and
report invalid parameters so the existing caller stops.

## Definition of done

- [x] Overlong effective image prompts fail before any vendor request.
- [x] Valid prompt and avoidance text retain their exact bytes.
- [x] Vendor code 2013 is an invalid parameter error, separate from content rejection.

## Steps

- [x] Check collisions: earlier broad provider/tests scope was PR #1172, already merged.
- [x] Implement the image-only joined prompt guard; preserve video prompt behavior.
- [x] Run focused provider/job tests, Ruff and type checks.

## How to verify

Run `uv run pytest tests/test_video_media_providers.py tests/test_video_media_jobs.py`,
Ruff for the changed files and the API mypy checks. The regression asserts zero
HTTP calls at the limit and exact retention below it, including Unicode inputs.

## Notes

- Official references checked 2026-10-04: MiniMax image-generation-t2i lists a
  1500-character limit; errorcode identifies 2013 as invalid parameters.
  https://platform.minimax.io/docs/api-reference/image-generation-t2i
  https://platform.minimax.io/docs/api-reference/errorcode
- Live endpoint detail is `prompt length must be less than 1500`, so reject the
  boundary as well. Do not silently discard avoidance text in the normal adapter.
- No settings, old job attempts, receipts or global cost caps are modified.
- Validation: 85 provider/job tests passed; changed-file Ruff and full mypy
  checks passed (461 app files, 364 test files). Production deployment pending.
