---
id: 2026-10-05-speech-api-tells-a-provider-answer
title: Speech API tells a provider answer lost after sending apart from a provider failure
status: done
priority: P1
area: api
owner: claude-opus-5-5-speech-lost
claimed_at: 2026-10-07T01:52:00Z
created_at: 2026-10-05T04:47:59Z
completed_at: 2026-10-07T01:57:41Z
branch: claude/happy-carson-c1hy91
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

## 2026-10-07 implementation (claude-opus-5-5-speech-lost)

- `azure.py` gains `SpeechAnswerLost` (a `SpeechUpstreamError` with status 504), `NEVER_SENT`
  (`ConnectError`, `ConnectTimeout`, `PoolTimeout`, `UnsupportedProtocol`, `LocalProtocolError`)
  and `paid_request_failed()`. Azure and Gemini synthesis and Gemini transcription use it: never
  sent stays 502 `video_speech_upstream_failed`; any other `httpx.HTTPError` (read or write
  timeout, read error, protocol error, dropped connection) is 504 `video_speech_upstream_lost`.
  The free voices GET is unchanged.
- Synthesis keeps the reserved characters on a lost answer, since the provider may have billed
  them; never sent and the provider's own answers still give them back.
- Transcription checks `SpeechAnswerLost` before its status mapping, so a lost answer is not
  confused with Google's own 504, which stays 503 `video_speech_upstream_busy`.
- The judge leg needed no API change: since #1254 (landed in #1348) `JevClient._send` raises
  `JevOutcomeUncertain` for every lost answer, answered 502 `video_judge_outcome_uncertain`, and
  what still reaches `video_judge_upstream_failed` is a connection that never opened, a request
  httpx would not write, or a 429/529 Jev refused.
- The client needed no logic change: both new codes are paid 5xx outside `SETTLED_CODES`, so
  they are already `SPEECH_UNCERTAIN`. Its comment is rewritten and `client.test.mjs` gains
  both codes in the lost-answer table. An older host still answers `video_speech_upstream_failed`
  for a lost answer, which the client still resends, so nothing changes until this deploys.
- Verified: ruff, `mypy app`, `mypy tests`, the three speech test files (55 pass), and
  `node --test tools/video/tts/client.test.mjs tools/video/tts/tts.test.mjs` (41 pass);
  `npm run test:tools` 1981 pass.
- The claim was written by hand: `claim` refused because on main the review-held jev-judge ticket still covers admin_api.py; that ticket is closed in #1357.
