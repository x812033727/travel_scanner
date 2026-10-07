---
id: 2026-10-07-aligned-azure-synthesis-answers-a-timed
title: Aligned Azure synthesis answers a timed-out request as a settled failure
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-07T01:58:14Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_speech/align.py
  - apps/api/app/video_speech/align_api.py
  - apps/api/tests/test_video_speech_align.py
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

- [ ] A timed-out aligned synthesis answers 504 `video_speech_upstream_lost` and keeps the reserved
  characters; a cancellation Azure itself reports (`_status_of`) keeps its current mapping.
- [ ] The tool does not send it again (it already treats an unlisted paid 5xx as uncertain; add a
  case to `tools/video/tts/client.test.mjs` if a scope widening is agreed, otherwise note it).

## Steps

- [ ] Raise `SpeechAnswerLost` (apps/api/app/video_speech/azure.py) from the timeout branch, or an
  align-specific equivalent, and map it before `_refusal_for` in `align_api.py`.
- [ ] Decide whether an SDK cancellation with a connection-failure code can be told apart as never
  sent; if not, leave it as it is and say so here.
- [ ] Test in `test_video_speech_align.py` with a patched `synthesize_with_boundaries_blocking`
  that sleeps past the timeout.

## How to verify

From `apps/api`: `uv run ruff check .`, `uv run mypy app`, `uv run mypy tests`,
`uv run pytest tests/test_video_speech_align.py`. No live provider is called.

## Notes

- Found while doing 2026-10-05-speech-api-tells-a-provider-answer (2026-10-07).
