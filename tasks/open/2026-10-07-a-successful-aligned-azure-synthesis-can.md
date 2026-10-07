---
id: 2026-10-07-a-successful-aligned-azure-synthesis-can
title: A successful aligned Azure synthesis can return before its last boundary events arrive
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-10-07T09:11:57Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_speech/align.py
  - apps/api/tests/test_video_speech_align.py
---

# A successful aligned Azure synthesis can return before its last boundary events arrive

## Why

`POST /video/speech/align` with an Azure voice synthesizes the line through the Speech SDK and
answers its audio together with when each written unit is spoken. It measures those times from
the SDK's `synthesis_word_boundary` events (`apps/api/app/video_speech/align.py`
`synthesize_with_boundaries_blocking`). The SDK fires those events on its own thread.
`speak_ssml_async(ssml).get()` can return the completed result before the last of them have
reached the callback. The function then reads `boundaries` too early.

The review of `2026-10-07-speech-align-route-tells-an-azure` measured this with the real SDK
1.52 against a local stand-in for the service's websocket. The stand-in sent turn.start, three
boundaries, 600 ms of audio and turn.end back to back:

- In 5 of 30 runs, the function returned 0 of 3 boundaries, and in 1 run, 2 of 3. The rest
  arrived after it had returned.
- Through the route, 1 run of 8 answered 200 with the units' times split evenly (the estimate)
  instead of the measured ones.
- A paced stream (audio in 20 ms steps, turn.end 30 ms after the last chunk) gave all three
  boundaries in 30 of 30 runs.

So how often the real service triggers this is unknown. When it does, the karaoke captions of a
Short or a long video's measured cue times fall back to an estimate without any sign of it.
Nothing is billed twice: this is the timing only.

## Definition of done

- [ ] A completed aligned synthesis returns every boundary the SDK delivers for it, even when the
  events reach the callback after `.get()` returns.

## Steps

- [ ] After `.get()`, wait (bounded, e.g. one second) for a `threading.Event` that the
  synthesizer's `synthesis_completed` and `synthesis_canceled` signals set, and only then read
  `boundaries`. In the stand-in run above, that made the burst success 30 of 30.
- [ ] Teach `FakeSdk` in `tests/test_video_speech_align.py` to fire some boundary events after
  `get()` returns, followed by the completion signal. Test that all of them are returned, and
  that a completion signal which never comes costs at most the bound.

## How to verify

From `apps/api`: `PYTHONUTF8=1 uv run pytest tests/test_video_speech_align.py`, then `uv run
ruff check .` and `uv run mypy app tests`. A run against a local websocket stand-in, like the one
the review used, shows the burst case returning every boundary.

## Notes

- Found by the check of the review fixes for `2026-10-07-speech-align-route-tells-an-azure`
  (2026-10-07). It is older than that task: the same happened at its first commit and with the
  SDK's own retry left on.
- A cancelled synthesis is not affected. That task reads the SDK's `USP state` from the error text
  as well, so a boundary that reaches its callback late still makes the cancellation lost.
