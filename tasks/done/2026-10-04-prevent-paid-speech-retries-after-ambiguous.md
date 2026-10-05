---
id: 2026-10-04-prevent-paid-speech-retries-after-ambiguous
title: Prevent paid speech retries after ambiguous transport outcomes
status: done
priority: P1
area: tools
owner: claude-opus-5-5-tts-client-paid-retries
claimed_at: 2026-10-05T00:13:38Z
created_at: 2026-10-04T15:41:30Z
completed_at: 2026-10-05T00:49:01Z
branch: claude/tts-client-paid-retries
depends_on: []
scope:
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
  - docs/videos/imported-long-languages/speech-journal.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# Prevent paid speech retries after ambiguous transport outcomes

## Why

The shared speech client retries a thrown fetch error and general 5xx responses inside `call`, with five attempts by default. For paid synthesis, transcription or judge POSTs, the server may have completed work before the connection lost its answer. Unlike the automation run client, this path does not distinguish a request never sent from an uncertain paid outcome. A retry can therefore pay for the same input again. This was found by source inspection during AI-series production; no duplicate charge is claimed.

## Definition of done

- [ ] A paid request whose outcome is unknown stops and records enough input identity to reconcile; it is never blindly resent.
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
- Settled codes, checked in `apps/api/app/video_speech/admin_api.py` and `checking.py`, keep
  the bounded retry: `video_speech_upstream_busy` (429/503, provider refused or overloaded),
  `video_speech_upstream_failed` (502, synthesis releases the reserved characters first),
  `video_speech_upstream_rejected_key` (502, provider 401/403) and `video_judge_upstream_failed`
  (502, Jev failed behind the API). `rate_limit_exceeded` is a 429 before any work and keeps its
  retry. They are settled only when the API reached the provider's answer or never connected:
  see the review section below for the case they do not cover. `upstream_unavailable` is NOT
  settled for the speech routes: `apps/web/app/api/video/speech/forward.ts` answers it both for
  an API it never reached and for one whose answer it lost after 180 s or a dropped connection,
  because the speech routes pass no `LostAnswer` (the automation run route does, which is why
  the automation client may treat it as settled). Filed 2026-10-05-speech-routes-lost-paid-answer
  to fix that at the route; until then an API restart behind a live web container stops a paid
  request for the owner (the video is blocked) instead of retrying it.
- `who` is "owner" (exit 3). Caller audit, completed in the review round below: `tts` blocks the
  video on any non-zero exit; `tts/check.mjs` lets only "service" errors through as unchecked
  lines, so an uncertain transcription or judgement stops `check-audio` (exit 3);
  `shorts/speech.mjs` and `shorts/check.mjs` let it propagate to the Shorts lab; `dub` and
  `check-audio --locale` exit 3 used to give the language up for good, and `check-audio` exit 3
  for the narration used to fall through to `review-push`, both now changed in `flow.mjs`; the
  imported-long-languages runner (`docs/videos/imported-long-languages/runner.mjs`, its
  `createSpeechJournalFetch` wraps this client) turns exit 3 into a `HardStop`. No caller retries
  a SpeechError itself within a run.
- Owner codes, 401, `video_speech_budget_exhausted` and `jev_budget_exhausted` keep their
  meaning and stop after one request; `tools/video/tts/tts.test.mjs` (receipt-bound, unchanged)
  still sees five calls for five 502 `video_speech_upstream_failed`.
- Left for others: a later run does not know that an earlier one sent the request. The main
  worker does not resend on its own (it blocks the video until the owner retries), but the
  Shorts lab re-runs a phase next round after any owner error:
  2026-10-05-reuse-confirmed-speech-results-across-restart (durable journal and holds).

### 2026-10-05 review round 1 (claude-opus-5-5-tts-client-paid-retries)

Independent review of PR #1235 found four problems; all are fixed or split here.

- DoD 1 is unticked. `video_speech_upstream_failed` and `video_judge_upstream_failed` are also
  what the API answers when the request to the provider was already sent and its answer was
  lost: `azure.py`, `gemini.py` and `checking.py` turn any `httpx.HTTPError` (a `ReadTimeout`
  after 90 s Azure or 150 s Gemini, a `RemoteProtocolError`, a `ReadError`) into a 502, and
  `admin_api.py` answers Jev's `httpx.HTTPError` the same way after `consume_jev_call` spent a
  daily call. Giving the reserved characters back does not settle the provider's bill, so such a
  request is still resent up to four more times, as it was on main. The client cannot tell the
  two apart; the API half is split into 2026-10-05-speech-api-tells-a-provider-answer (P1),
  which gives that case its own code for the client to treat as uncertain. The earlier note that
  every settled code is "the API's own answer once the attempt is over" was wrong.
- The first caller audit missed `docs/videos/imported-long-languages/runner.mjs`. Its reviewed
  suite went red: `speech-journal.test.mjs` expected a 503 `upstream_unavailable` behind the
  journal to end as `video_speech_result_held` (who "service", exit 4); it now ends as
  `video_speech_uncertain` (who "owner", exit 3), still after one POST with the journal entry
  "unknown". The test expectation is updated (scope widened for it). In the runner, exit 3 is a
  `HardStop` (runner.mjs, `code === EXIT.owner`) where exit 4 used to come back to the flow; no
  second POST is sent either way.
- `dub` and `check-audio --locale` exit 3 gave the language up for good (`giveUpDub` writes
  `dubs/<locale>/skipped.json`, and a skipped locale is never made again), so a reset socket or
  a gateway 502/504 during a deploy would have dropped a dub that may well have worked.
  `flow.mjs` now reads the code in the command's last line (`speechUncertain`: exit 3 and
  `video_speech_uncertain`, which the client's one-line message now ends with) and blocks the
  video instead, for `dub`, its retake and its check. The locale is marked `check_stopped`, so
  the owner's retry makes it again with its check, though its track may read as current (the
  same mark PR #1242 adds for a STOP file). Other exit 3s (a voice that speaks one language, no
  Gemini key) still give the locale up. Scope widened to `flow.mjs` and `automation.test.mjs`.
- The narration's `check-audio` exit 3 went on to `review-push` with a half-written check.json;
  fixed with 2026-10-05-narration-review-after-check-audio-owner in the same PR.
- Verified: `node --test tools/video/tts/client.test.mjs` (6 pass; the uncertain message is one
  line ending with the code), `node --test docs/videos/imported-long-languages/*.test.mjs`
  (115 pass; 113 of 115 before the fix), and the new flow test in
  `tools/video/automation/automation.test.mjs` (a dub blocked twice by a lost synthesis and a
  lost judgement, made and checked after the owner's retries, while a plain owner exit 3 still
  gives ko up).
