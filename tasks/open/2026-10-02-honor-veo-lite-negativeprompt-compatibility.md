---
id: 2026-10-02-honor-veo-lite-negativeprompt-compatibility
title: Honor Veo Lite negativePrompt compatibility
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-02T19:02:53Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_media/providers/gemini_video.py
  - apps/api/tests/test_video_media_providers.py
---

# Honor Veo Lite negativePrompt compatibility

## Why

`GeminiVideo.request_body` already handles several capabilities of
`veo-3.1-lite-generate-preview`, but it still sends `parameters.negativePrompt`
whenever a request has a negative prompt. On 2026-10-03, the E1 S01 pilot and its
separately authorized diagnostic submit failed before returning an operation.
The diagnostic for job `fc63bb73-174e-49ee-96c1-23a1289541fa` obtained HTTP 400
`INVALID_ARGUMENT`: `negativePrompt` is not supported by this model. This is a
confirmed parameter-compatibility failure; it is not evidence of a content safety
rejection.

The production owner submitted a separately bound R03 manifest that omits the
unsupported field while preserving the same scene constraints in the main prompt.
The HTTP response became 200 and job `340951d1-4f13-43fb-91fe-c6f42c40f032` later
returned a ready file. Later visual QA rejected that file for a second watch and
extra hand movement; transport success is separate from usable footage. The
scoped workaround does not repair the shared adapter for future Lite jobs.

## Definition of done

- [ ] Lite requests never send the unsupported `parameters.negativePrompt` field, while preserving the requested scene constraints through supported input rather than silently dropping them.
- [ ] The handling is specific to verified model capabilities; other video models retain their supported request behavior.
- [ ] Existing Lite rules for first frames, reference images, 1080p/eight-second requests and native audio remain covered.
- [ ] `personGeneration=allow_adult`, model choice, source frames, provider host/key safeguards, approval/budget guards and retry/reservation behavior are unchanged.
- [ ] Offline request-body tests reproduce the unsupported field and verify the corrected model-specific payload without a paid call.

## Steps

- [ ] Recheck the pinned Lite model's supported inputs against official API documentation and the sanitized captured `INVALID_ARGUMENT` evidence.
- [ ] Add a regression in the existing provider test file covering Lite with a negative prompt, preserved constraints, and a non-Lite request that still supports its existing field.
- [ ] Implement the narrow request-body compatibility fix, with no model fallback, safety relaxation, automatic retake or production configuration change.

## How to verify

```bash
cd apps/api
uv run pytest tests/test_video_media_providers.py -q
uv run ruff check app/video_media/providers/gemini_video.py tests/test_video_media_providers.py
```

Inspect generated request bodies under the existing mock transport. No live model
invocation is needed to verify omission of an unsupported parameter.

## Notes

- Filed only, intentionally `open` and unclaimed; no provider code was changed in this reporting task.
- Searched current tasks/open for Lite, negativePrompt and unsupported-parameter work; no existing ticket covered this compatibility gap. Scope checks found no active task or open PR touching `gemini_video.py` or the provider test file at filing time; recheck before claiming.
- `2026-10-02-preserve-sanitized-video-provider-rejection-details` separately covers discarded provider diagnostics. Both tickets use `test_video_media_providers.py`, so coordinate sequential claims or explicitly combine their test work; do not race the file.
- The failed diagnostic still consumed a conservative reservation. Keep its failed job and receipts; do not replay it or treat the generic app classification `blocked` as a reason to bypass safety checks.
- Local sanitized evidence is referenced by `docs/videos/series-plans/competition-20261002/episodes/production-run-20261003.md`; original provider credentials and request image data remain outside Git.
- Verified local `diagnostic-r02/transport.jsonl` SHA-256 `0111f51712753cb8ed6578b248b82317a3b2d0c2b85f571b04ab663b84f16f47` records HTTP 400 / `INVALID_ARGUMENT` and explicitly identifies unsupported `negativePrompt`. R03 `diagnostic-r03/transport.jsonl` SHA-256 `3b24d7859fa89081a5a41b8a71406eeb458e146fbc8054bde19d24529e317d99` records HTTP 200 after removing that API field; all avoidance text was retained in the main prompt.
