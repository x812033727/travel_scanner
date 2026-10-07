---
id: 2026-10-07-aligned-azure-synthesis-answers-a-timed
title: Aligned Azure synthesis answers a timed-out request as a settled failure
status: done
priority: P2
area: api
owner: claude-opus-5-5-speech-lost
claimed_at: 2026-10-07T02:00:13Z
created_at: 2026-10-07T01:58:14Z
completed_at: 2026-10-07T02:01:05Z
branch: claude/happy-carson-c1hy91
depends_on: []
scope:
  - apps/api/app/video_speech/azure.py
  - apps/api/app/video_speech/align.py
  - apps/api/app/video_speech/align_api.py
  - apps/api/tests/test_video_speech_align.py
  - tools/video/tts/client.test.mjs
---

# Aligned Azure synthesis answers a timed-out request as a settled failure

## Why

`apps/api/app/video_speech/align.py` (`synthesize_with_boundaries`) runs the Azure Speech SDK on a
worker thread and turns the route's `asyncio.wait_for` timeout into
`SpeechUpstreamError(502, "Azure Speech did not answer in time")`. By then the SDK has usually
sent the SSML, so Azure may have synthesized and billed it. `align_api.py` (`_synthesize_azure`)
then gives the reserved characters back and `_refusal_for` answers 502
`video_speech_upstream_failed`, which `tools/video/tts/client.mjs` counts as settled and sends
again (`synthesizeAligned`). The thread is not cancelled either, so the first synthesis can still
finish while the retry runs.

The plain speech routes got their own code for this case in
2026-10-05-speech-api-tells-a-provider-answer: 504 `video_speech_upstream_lost`, characters kept,
not resent by the client. This route was outside that ticket's scope.

## Definition of done

- [x] A timed-out aligned synthesis answers 504 `video_speech_upstream_lost` and keeps the reserved
  characters; a cancellation Azure itself reports (`_status_of`) keeps its current mapping.
- [x] The tool does not send it again (it already treats an unlisted paid 5xx as uncertain; add a
  case to `tools/video/tts/client.test.mjs` if a scope widening is agreed, otherwise note it).

## Steps

- [x] Raise `SpeechAnswerLost` (apps/api/app/video_speech/azure.py) from the timeout branch, or an
  align-specific equivalent, and map it before `_refusal_for` in `align_api.py`.
- [x] Decide whether an SDK cancellation with a connection-failure code can be told apart as never
  sent; if not, leave it as it is and say so here.
- [x] Test in `test_video_speech_align.py` with a patched `synthesize_with_boundaries_blocking`
  that sleeps past the timeout.

## How to verify

From `apps/api`: `uv run ruff check .`, `uv run mypy app`, `uv run mypy tests`,
`uv run pytest tests/test_video_speech_align.py`. No live provider is called.

## Notes

- Found while doing 2026-10-05-speech-api-tells-a-provider-answer (2026-10-07).
- 2026-10-07 (claude-opus-5-5-speech-lost): `synthesize_with_boundaries` raises
  `SpeechAnswerLost("Azure Speech", TimeoutError)` on the route's deadline; `_synthesize_azure`
  catches it before `SpeechUpstreamError`, keeps the reservation and answers 504
  `video_speech_upstream_lost` through `AlignRefused`. `SpeechAnswerLost` now takes any
  exception as its cause, so azure.py joined the scope.
- SDK cancellations keep their mapping. `CancellationErrorCode.ConnectionFailure` does not say
  whether the SSML left before the socket failed, and `ServiceTimeout` is Azure's own answer;
  neither can be told apart as never sent, so they stay `video_speech_upstream_failed` (502) as
  before. Revisit only if a duplicate charge is ever seen from one.
- The client needed no change and no new case: `synthesizeAligned` is in the PAID table of
  `client.test.mjs`, which runs the 504 `video_speech_upstream_lost` row added by the previous
  ticket for every paid request.
- Verified: ruff, `mypy app`, `mypy tests`, the four speech test files (73 pass),
  `node --test tools/video/tts/client.test.mjs`.
