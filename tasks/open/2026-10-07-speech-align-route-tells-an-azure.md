---
id: 2026-10-07-speech-align-route-tells-an-azure
title: Speech align route tells an Azure synthesis lost after sending apart from a provider failure
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-10-07T04:32:22Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_speech/align.py
  - apps/api/app/video_speech/align_api.py
  - apps/api/tests/test_video_speech_align.py
  - tools/video/tts/client.test.mjs
---

# Speech align route tells an Azure synthesis lost after sending apart from a provider failure

## Why

`POST /video/speech/align` with an Azure voice is paid: it synthesizes the line through the
Speech SDK and returns the audio with its word timings (`tools/video/tts/client.mjs`
`synthesizeAligned` sends it with `paid: true`). The client sends a paid request again only when
the API settled it, and it counts 502 `video_speech_upstream_failed` as settled.

The align route answers that code for a synthesis whose outcome it cannot tell:

- `apps/api/app/video_speech/align.py` (`synthesize_with_boundaries`) turns the route's
  `asyncio.wait_for` timeout into `SpeechUpstreamError(502, "Azure Speech did not answer in
  time")`. The worker thread is not cancelled by that timeout, so the SDK's synthesis can still
  finish, and be billed, after the route has answered.
- A cancellation whose SDK error code means the connection failed mid-synthesis maps through
  `_status_of` to a status that `_refusal_for` in `align_api.py` answers as 502
  `video_speech_upstream_failed`.
- Both release the reserved characters, as for a refused request.

So an aligned synthesis whose outcome is unknown is resent up to four more times. The plain
speech route got its own code for this case in
2026-10-05-speech-api-tells-a-provider-answer (504 `video_speech_upstream_lost`, a new
`SpeechAnswerLost` in `azure.py`); the align route was outside that task's scope.

## Definition of done

- [ ] The align route answers an Azure synthesis that may have run without a usable answer (its
  own timeout, a connection the SDK reports lost after it started) with 504
  `video_speech_upstream_lost`, keeping the characters counted, and keeps
  `video_speech_upstream_failed` for a synthesis that certainly never started.
- [ ] `tools/video/tts/client.test.mjs` shows `synthesizeAligned` sending such an answer once
  (it already does for any 5xx that is not settled; the test pins it for the align path).

## Steps

- [ ] Find which `CancellationErrorCode` values mean nothing was sent (a connection that never
  opened, an auth failure) and which may follow a request Azure ran (`ConnectionFailure` mid-way,
  `ServiceTimeout`, `ServiceError`). Write down what the SDK documents and what you could not
  prove; an unknown one counts as lost.
- [ ] Raise `SpeechAnswerLost` (from `app/video_speech/azure.py`) for the lost ones and the
  route's timeout, and answer it in `align_api.py` as the speech route does
  (`admin_api.answer_lost`).
- [ ] Tests in `test_video_speech_align.py` for both sides, with the SDK stubbed as the file
  already does.

## How to verify

From `apps/api`: `uv run ruff check .`, `uv run mypy app`, `uv run mypy tests` and
`PYTHONUTF8=1 uv run pytest tests/test_video_speech_align.py`. From the root:
`node --test tools/video/tts/client.test.mjs`. No live provider is called.

## Notes

- Found while doing 2026-10-05-speech-api-tells-a-provider-answer (2026-10-07).
- `alignClip` (any clip, `speech/align` with `audio`) is not paid and is not affected.
