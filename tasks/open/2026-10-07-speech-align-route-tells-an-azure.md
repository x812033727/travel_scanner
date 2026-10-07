---
id: 2026-10-07-speech-align-route-tells-an-azure
title: Speech align route tells an Azure synthesis lost after sending apart from a provider failure
status: in-progress
priority: P2
area: api
owner: claude-opus-5-5-align-lost
claimed_at: 2026-10-07T07:28:49Z
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

- [x] The align route answers an Azure synthesis that may have run without a usable answer (its
  own timeout, a connection the SDK reports lost after it started) with 504
  `video_speech_upstream_lost`, keeping the characters counted, and keeps
  `video_speech_upstream_failed` for a synthesis that certainly never started.
- [x] `tools/video/tts/client.test.mjs` shows `synthesizeAligned` sending such an answer once
  (it already does for any 5xx that is not settled; the test pins it for the align path).

## Steps

- [x] Find which `CancellationErrorCode` values mean nothing was sent (a connection that never
  opened, an auth failure) and which may follow a request Azure ran (`ConnectionFailure` mid-way,
  `ServiceTimeout`, `ServiceError`). Write down what the SDK documents and what you could not
  prove; an unknown one counts as lost.
- [x] Raise `SpeechAnswerLost` (from `app/video_speech/azure.py`) for the lost ones and the
  route's timeout, and answer it in `align_api.py` as the speech route does
  (`admin_api.answer_lost`).
- [x] Tests in `test_video_speech_align.py` for both sides, with the SDK stubbed as the file
  already does.

## How to verify

From `apps/api`: `uv run ruff check .`, `uv run mypy app`, `uv run mypy tests` and
`PYTHONUTF8=1 uv run pytest tests/test_video_speech_align.py`. From the root:
`node --test tools/video/tts/client.test.mjs`. No live provider is called.

## Notes

- Found while doing 2026-10-05-speech-api-tells-a-provider-answer (2026-10-07).
- `alignClip` (any clip, `speech/align` with `audio`) is not paid and is not affected.
- 2026-10-07 (claude-opus-5-5-align-lost). What the SDK (1.52, `enums.py`) documents for each
  `CancellationErrorCode`, what it reports in practice, and how `align.py` `_cancellation` reads
  it. Measured with the real SDK against a local stand-in for the service's websocket, during
  the review below:
  - The SDK retries a synthesis cancelled before any audio by itself
    (`SpeechSynthesis_MaxRetryTimes`, on by default) and reports only the last try. So a
    reconnect that failed or was refused after a first try had sent the SSML read as "never
    opened" or as a 429 or 503, and one call could send the SSML twice. `speech_config` now sets
    it to 0: each cancellation describes the one try, and the video tool's own settled-only
    resend decides what is sent again.
  - The SDK takes the code from the websocket's close code alone, whatever had happened by then.
    A 1011 after 19,200 bytes of audio is `ServiceError`, and a 4429 after audio is
    `TooManyRequests`. A cancelled result keeps the audio that came first, and has no bytes at
    all when none came. So a result with audio or a boundary event is lost whatever its code.
  - Settled when nothing had arrived: `AuthenticationFailure` (401), `Forbidden` (403),
    `BadRequest` (400) and `TooManyRequests` (429). These are the service's refusals before it
    synthesizes, and a 4429 is its concurrency throttle. Nothing documents that a refusal is
    billed.
  - `ServiceUnavailable` (503) and `ServiceError` (502) are settled only when the websocket's
    upgrade was refused ("WebSocket upgrade failed: ..."), before any SSML went out. A socket
    the service closed after taking the SSML is lost, even before the turn started.
  - `ConnectionFailure` is settled only when the text says the socket never opened
    (`WS_OPEN_ERROR...`, "no connection to the remote host", or a refused upgrade). A drop after
    it opened ("WebSocket operation failed ... WS_ERROR_UNDERLYING_IO_ERROR", a 1006 close, a
    frame that failed to send) is lost.
  - Lost: `ServiceTimeout`, `RuntimeError`, the two internal redirects, `EmbeddedModelError`
    (not used here), and any code this module does not know.
  - The rules read the whole error text; the message keeps its first 200 characters.
  - The route's own `asyncio.wait_for` timeout is lost too: the worker thread is not cancelled, so
    the synthesis can still finish and be billed.
- `align_api.py` `_synthesize_azure` answers `SpeechAnswerLost` as 504 `video_speech_upstream_lost`
  without releasing the reservation, before the `SpeechUpstreamError` handler that releases it.
- `client.test.mjs` needed no change: its lost-answer table already runs every paid call,
  `synthesizeAligned` included, through a 504 `video_speech_upstream_lost` and checks it is sent
  once, held as `SPEECH_UNCERTAIN`.
- Tests (`test_video_speech_align.py`), with the SDK's own texts:
  - Settled: each refusal, a refused upgrade for every code, a socket that never opened.
  - Lost: a service timeout, a drop or 1006 after the socket opened, a frame that failed to send,
    a 1011 at Sending or TurnStarted, a service down after the socket opened, a runtime error,
    and an unknown code.
  - Lost whatever the code, once audio or a boundary had come: a 4429, 1011 or 1007 after audio,
    and a boundary before any audio.
  - The rules read past the message's 200 characters.
  - The blocking synthesis turns the SDK's retry off.
  - With the real SDK: `speech_config` sets the property, and every code name the rules and the
    fake use is one of the SDK's.
  - The route test checks the 504 and that the characters stay counted.
  - Each was checked against a mutation, and each mutation fails: settling the timeout, every
    `ConnectionFailure`, an unknown code, `ServiceTimeout`, or `ServiceError` or
    `ServiceUnavailable` whatever their text; ignoring the audio or the boundaries; reading only
    200 characters; leaving the retry on; releasing the characters on a lost answer; answering it
    as `upstream_failed`; dropping its handler.
  - End to end, the real SDK and `synthesize_with_boundaries_blocking` ran against the stand-in.
    Every settled case had sent no SSML frame, every lost case had sent one, and each made one
    connection.
- Review (2026-10-07, three lenses, each finding verified):
  - Blocking: `ServiceError` was settled although the SDK reports it for a 1011 after audio.
  - Should-fix: the SDK's own retry (above).
  - Should-fix: a result that had started must be lost whatever its code.
  - All three are fixed as described. Refuted or not needed: settling more never-opened texts
    under other codes (only safe with the retry off, and the trade the task asks for); a 4429 or
    1007 after audio in practice (covered anyway by the audio rule); a missing SDK after the
    reservation (the package is in the lock and the image).
