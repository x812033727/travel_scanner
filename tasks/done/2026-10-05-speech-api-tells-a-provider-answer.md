---
id: 2026-10-05-speech-api-tells-a-provider-answer
title: Speech API tells a provider answer lost after sending apart from a provider failure
status: done
priority: P1
area: api
owner: claude-opus-5-5-speech-lost
claimed_at: 2026-10-07T04:23:15Z
created_at: 2026-10-05T04:47:59Z
completed_at: 2026-10-07T05:01:15Z
branch: claude/sharp-bardeen-ob6fn9
depends_on: []
scope:
  - apps/api/app/video_speech/azure.py
  - apps/api/app/video_speech/gemini.py
  - apps/api/app/video_speech/checking.py
  - apps/api/app/video_speech/admin_api.py
  - apps/api/tests/test_video_speech.py
  - apps/api/tests/test_video_speech_gemini.py
  - apps/api/tests/test_video_speech_check.py
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
  - tools/video/shorts/lab.mjs
  - tools/video/shorts/lab.test.mjs
---

# Speech API tells a provider answer lost after sending apart from a provider failure

## Why

`tools/video/tts/client.mjs` sends a paid speech request (`speech`, `speech/transcribe`,
`speech/judge`) again only when it never left or the API settled it. It counts
`video_speech_upstream_failed` and `video_judge_upstream_failed` as settled, but the API also
answers those codes when the request to the provider was already sent and its answer was lost:

- `apps/api/app/video_speech/azure.py` (`synthesize`) and `gemini.py` (`synthesize`) turn any
  `httpx.HTTPError` into `SpeechUpstreamError(502)`, a `ReadTimeout` after 90 s (Azure) or 150 s
  (Gemini), a `RemoteProtocolError` or a `ReadError` included; `admin_api.py` answers it as 502
  `video_speech_upstream_failed`. The reserved characters are given back, but the provider may
  have synthesized and billed the request.
- `checking.py` (`transcribe`) does the same for Gemini transcription.
- `admin_api.py` (`judge_narration`) answers any `httpx.HTTPError` from Jev as 502
  `video_judge_upstream_failed`, after `consume_jev_call` has spent a daily call.

So a paid request whose provider outcome is unknown is still resent up to four more times by the
client. This is the part of 2026-10-04-prevent-paid-speech-retries-after-ambiguous that the
client alone cannot do (split from it, DoD 1). Found by review of PR #1235 on 2026-10-05; no
duplicate charge has been seen. The behaviour for these codes is the same as on main before that
PR (main resent every failure), so it does not block that PR.

## Definition of done

- [x] The three speech routes answer a provider error after the request was sent (a read
  timeout, a read or protocol error, a dropped connection) with their own code, for example 504
  `video_speech_upstream_lost` and `video_judge_upstream_lost`, and keep
  `video_speech_upstream_failed` / `video_judge_upstream_failed` for connect errors and definite
  provider 5xx answers.
- [x] The client treats the new codes as `SPEECH_UNCERTAIN` (sent once, exit 3, the video
  blocked for the owner); `upstream_failed` stays retried, so
  `tools/video/tts/tts.test.mjs` (receipt-bound) keeps its five calls.
- [x] A client newer than the host stays safe: until the API change is deployed the client's
  behaviour for the old codes does not change.

## Steps

- [x] Split `httpx.ConnectError` / `httpx.ConnectTimeout` (nothing sent) from the other
  `httpx.HTTPError`s in `azure.py`, `gemini.py` and `checking.py`, and from Jev's in
  `admin_api.py` (check what `JevClient.ask` raises for each; `JevError` may wrap them).
- [x] API tests for both sides in `test_video_speech.py`, `test_video_speech_gemini.py` and
  `test_video_speech_check.py` (an `httpx.MockTransport` raising `ReadTimeout` versus
  `ConnectError`).
- [x] Add the new codes to the client's uncertain path in `tools/video/tts/client.mjs` with a
  case in `client.test.mjs`.

## How to verify

From `apps/api`: `uv run ruff check .`, `uv run mypy app`, `uv run mypy tests` and
`PYTHONUTF8=1 uv run pytest tests/test_video_speech.py tests/test_video_speech_gemini.py
tests/test_video_speech_check.py`. From the root: `node --test tools/video/tts/client.test.mjs
tools/video/tts/tts.test.mjs`. No live provider is called.

## Notes

- Split from 2026-10-04-prevent-paid-speech-retries-after-ambiguous (PR #1235 review, finding
  on `SETTLED_CODES`).
- `video_speech_upstream_busy` (a provider 429, or a transcription 500/503/504 the provider
  answered) and `video_speech_upstream_rejected_key` (a provider 401/403) are the provider's own
  answers and can stay settled.
- Related: 2026-10-05-speech-routes-lost-paid-answer does the same one layer up, for the web
  route's 502 `upstream_unavailable`.
- Done 2026-10-07. `azure.py` has `SpeechAnswerLost` (deliberately not a `SpeechUpstreamError`,
  so a route that forgets it answers a 500, which the client also holds as uncertain) and
  `transport_failure()`: `httpx.ConnectError`, `ConnectTimeout` and `PoolTimeout` stay
  `SpeechUpstreamError(502, "<provider> unreachable: ...")`; every other `httpx.HTTPError` from
  the POST is `SpeechAnswerLost`. Azure and Gemini synthesis and Gemini transcription use it.
  `admin_api.answer_lost()` answers it as 504 `video_speech_upstream_lost`. Synthesis keeps the
  reserved characters counted for it, since the provider may have billed them; a never-sent
  failure still gives them back.
- Jev's half was already done by Codex #1254 (train #1348): `JevClient._send` raises
  `JevOutcomeUncertain` for anything after the request may have left, and `judge_narration`
  answers it as 502 `video_judge_outcome_uncertain`. What still reaches its
  `video_judge_upstream_failed` is a connection that never opened (after the client's one retry),
  a request httpx refused to write, a 429/529 refused every time, or another definite 4xx. So no
  `video_judge_upstream_lost` was added; `client.test.mjs` pins the 502
  `video_judge_outcome_uncertain` as uncertain instead.
- The client needed no code change: any paid 5xx outside `SETTLED_CODES` is already
  `SPEECH_UNCERTAIN`, so a host serving the 504 is held at once, and an older host's 502
  `video_speech_upstream_failed` is resent as before (`tts.test.mjs` still sees five calls). The
  comment above `SETTLED_CODES` and the tests' table now say so.
- Left alone, as definite answers rather than lost ones: a 2xx whose body is not audio (Azure)
  or has no transcript (Gemini's SAFETY block), and Jev's malformed answers block. They were
  billed, but asking again is a policy choice, not an unknown outcome.
- The align route (`speech/align`, paid for an Azure voice) has the same gap in its SDK path; it
  was outside this scope and is 2026-10-07-speech-align-route-tells-an-azure.
- An independent review (2026-10-07, four lenses, each finding verified) confirmed one should-fix
  outside the original scope. A Short (`shorts/lab.mjs` `LabShort.run`, which `CutShort` shares)
  treated `SPEECH_UNCERTAIN` like any other owner error: it printed "waits for the owner" to the
  worker's stdout and never called `block()`. So nothing reached /admin/videos, `next_job_for`
  kept naming it, and the owner's retry did not apply. This change sends every provider read
  timeout down that path, where before they were resent. The scope was widened to the two lab
  files, which no active task held: `run()` now blocks the Short on `SPEECH_UNCERTAIN`, the
  journal's later-round hold included, before the generic owner branch. The new
  `lab.test.mjs` test fails on the old code.
- Review nits taken: `UnsupportedProtocol` and `LocalProtocolError` are raised before a byte
  leaves, so they join `NEVER_SENT` as in `jev.py`. The tests also pin `WriteError` as lost and
  pin that `SpeechAnswerLost` is not a `SpeechUpstreamError`, and the transcription test's
  key-leak assertion now has the key to look for.
- Review nits left:
  - `automation.test.mjs` `ERROR_SCOPES` does not list the new 504 code. The default already
    puts it in the right scope ('wait', like `video_speech_answer_lost`), and the file is
    duration-bound and outside this scope.
  - Pre-existing: a refund (`release_azure_speech_characters` without `now`) is filed under the
    month at release time, not the reservation's month.
