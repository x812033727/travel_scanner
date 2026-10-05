---
id: 2026-10-04-prevent-paid-speech-retries-after-ambiguous
title: Prevent paid speech retries after ambiguous transport outcomes
status: in-progress
priority: P1
area: tools
owner: claude-opus-5-5-tts-client-paid-retries
claimed_at: 2026-10-05T00:13:38Z
created_at: 2026-10-04T15:41:30Z
completed_at:
branch: claude/tts-client-paid-retries
depends_on: []
scope:
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
---

# Prevent paid speech retries after ambiguous transport outcomes

## Why

The shared speech client retries a thrown fetch error and general 5xx responses inside `call`, with five attempts by default. For paid synthesis, transcription or judge POSTs, the server may have completed work before the connection lost its answer. Unlike the automation run client, this path does not distinguish a request never sent from an uncertain paid outcome. A retry can therefore pay for the same input again. This was found by source inspection during AI-series production; no duplicate charge is claimed.

## Definition of done

- [x] A paid request whose outcome is unknown stops and records enough input identity to reconcile; it is never blindly resent.
- [x] Definitive never-sent or server-settled failures retain the intended bounded recovery, and read-only status GETs can still retry.
- [x] Returned WAV/transcript/judge results and actual billed usage remain bound to their request; existing current caches are reused without forged evidence.

## Steps

- [x] Audit all shared POST callers and classify network errors, gateway errors, incomplete response bodies and settled provider failures.
- [x] Add source-bound reconciliation/recovery without changing provider, model, voice, budget or approvals.
- [x] Cover lost-after-send and lost-response-body cases with fake transport tests that assert one paid submission.

## How to verify

Run `node --test tools/video/tts/client.test.mjs` and relevant synthesis/audio callers. Use fake transports to prove ambiguous outcomes submit only once while safe failures and GETs retain their allowed recovery. Do not reproduce the failure against a paid provider.

## Notes

- `tools/video/tts/client.mjs:39` retries fetch exceptions; defaults at68 use five attempts. `synthesize` at103 sends the paid POST through that helper, then reads the WAV body. Shorts' `serverNarration` writes its cache only after a returned synthesis result.
- Existing `tools/video/automation/client.mjs` distinguishes never-sent and uncertain model runs; do not assume that protection already covers speech.
- The LLM episode's narration is complete and reused; no synthesis or paid retry was started after this finding. The current task leaves shared client files unchanged.

### 2026-10-05 done (claude-opus-5-5-tts-client-paid-retries, branch claude/tts-client-paid-retries)

- `call()` in `tools/video/tts/client.mjs` takes `paid`; `synthesize`, `transcribeClip` and
  `judgeLines` go through `postPaid`, `speechStatus` stays an unpaid GET. Same pattern as
  `tools/video/automation/client.mjs`: `NEVER_SENT` connect codes and `SETTLED_CODES` keep the
  bounded retry, everything else after a paid POST throws `SPEECH_UNCERTAIN`
  (`video_speech_uncertain`) at once, without a sleep or a second dispatch.
- Uncertain = a thrown fetch that is not a connect failure (ECONNRESET, UND_ERR_SOCKET, headers
  timeout), any 5xx without a settled code (a gateway's HTML 502/504, Starlette's bare 500, the
  web route's 502 `upstream_unavailable`), and a 200 whose body breaks off or cannot be read
  (`arrayBuffer`/`json`, the WAV decode, a `null` JSON). The answer read is inside `postPaid`, so
  a lost or corrupt body is never bought again either.
- The error carries the request: `error.path` and `error.requestSha256` (sha256 of the exact
  JSON body sent), both also in the one-line message that the CLIs print and the worker stores
  as its block reason. The server keeps no answer and takes no idempotency key, so
  reconciliation is a person comparing that hash with the provider's usage; nothing is fetched
  again automatically.
- Settled codes, checked in `apps/api/app/video_speech/admin_api.py` and `checking.py`: every
  one is the API's own answer once the attempt is over. `video_speech_upstream_busy` (429/503,
  provider refused or overloaded), `video_speech_upstream_failed` (502, synthesis releases the
  reserved characters first), `video_speech_upstream_rejected_key` (502, provider 401/403) and
  `video_judge_upstream_failed` (502, Jev failed behind the API). `rate_limit_exceeded` is a 429
  before any work and keeps its retry. `upstream_unavailable` is NOT settled for the speech
  routes: `apps/web/app/api/video/speech/forward.ts` answers it both for an API it never reached
  and for one whose answer it lost after 180 s or a dropped connection, because the speech
  routes pass no `LostAnswer` (the automation run route does, which is why the automation
  client may treat it as settled). Filed 2026-10-05-speech-routes-lost-paid-answer to fix that
  at the route; until then an API restart behind a live web container stops a paid request for
  a person instead of retrying it.
- `who` is "owner" (exit 3), chosen after the caller audit: `tts` blocks the video on any non-zero
  exit; `dub` exit 3 gives the language up with the reason in the notes while exit 4 would be
  tried again next round (a resend); `tts/check.mjs` lets only "service" errors through as
  unchecked lines, so an uncertain transcription or judgement stops `check-audio` (exit 3);
  `shorts/speech.mjs` and `shorts/check.mjs` let it propagate to the Shorts lab. No caller
  retries a SpeechError itself within a run, so no caller file changed.
- Owner codes, 401, `video_speech_budget_exhausted` and `jev_budget_exhausted` keep their
  meaning and stop after one request; `tools/video/tts/tts.test.mjs` (receipt-bound, unchanged)
  still sees five calls for five 502 `video_speech_upstream_failed`.
- Left for others: a later run does not know that an earlier one sent the request. The main
  worker does not resend on its own (it blocks the video or skips the dub), but the Shorts lab
  re-runs a phase next round after any owner error, and `check-audio` exit 3 currently falls
  through to `review-push` in `flow.mjs`. Both are in follow-ups:
  2026-10-05-reuse-confirmed-speech-results-across-restart (durable journal and holds) and
  2026-10-05-narration-review-after-check-audio-owner.
- Verified with `node --test tools/video/tts/client.test.mjs` (6 tests, every paid function
  against seven lost outcomes and nine settled ones, a counting fetch and a recording sleep).
