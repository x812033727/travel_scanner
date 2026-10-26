---
id: 2026-10-26-recover-ordinary-transcription-receipts
title: Recover ordinary transcription status results and ASR usage after lost POST answers
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-26T01:07:37Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
  - tools/video/tts/speech-journal.mjs
  - tools/video/tts/speech-journal.test.mjs
  - tools/video/tts/check-journal.test.mjs
  - apps/api/app/video_speech/admin_api.py
  - apps/api/app/video_speech/schemas.py
  - apps/api/app/video_speech/checking.py
  - apps/api/app/video_speech/transcription_receipts.py
  - apps/api/app/video_speech/models.py
  - apps/api/app/models.py
  - apps/api/migrations/versions/0138_video_transcription_receipts.py
  - apps/api/tests/test_video_speech_transcription_receipts.py
  - apps/api/tests/test_video_speech_check.py
  - apps/web/app/api/video/speech/transcribe/route.ts
  - apps/web/app/api/video/speech/requests/[requestId]/route.ts
  - apps/web/app/api/video/speech/route.test.ts
---

# Recover ordinary transcription status results and ASR usage after lost POST answers

## Why

An ordinary, non-pilot `speech/transcribe` POST can reach the server/provider but
lose its answer. The native client correctly holds that exact request instead of
blindly buying it again. However, this ordinary route has no durable request-level
status/result/ASR-usage recovery contract, so a healthy later status GET cannot
reconcile the lost answer or its possible charge.

On 2026-10-26, ForTy ES line `5nt9` sent a transcription at 00:21:10.700Z and
entered a held `video_speech_uncertain` state after HTTP 502 at 00:21:12.220Z.
The exact sent JSON SHA256 is
`9a361492e1a6bf205d1b8f7af3c8fa882ffc4d8b9c4ae937e68eb442a5cecd49`.
This is a local body fingerprint, not a provider request ID. No complete answer
or staged answer was found; the journal and the 19 cached transcripts remain.
The outcome and possible billing are **unknown**, not a proven failed/unbilled
request. This task does not resolve or authorize replay of that historical hold.

The preserved read-only diagnostic is
`forty-es-uncertain-native-capability-diagnostic.json`, SHA256
`02fff7ede6f66f5eea59dd894a532253db74630d7df31f05e7b1f60d37763a55`,
under the episode producer's external `work/ai-tech-next` evidence directory.
It records the ordinary API gap, original incident and unchanged archive; it
does not claim a provider charge or no charge.

## Definition of done

- [ ] An ordinary transcription has a durable request-specific identity and
      owner-authorized status/result/ASR-usage lookup. A completed result and
      obtained provider usage remain recoverable across a lost HTTP answer and
      API/client restart, bound to the exact audio/body/language/terms and caller.
- [ ] Reusing a logical request identity cannot dispatch a second paid provider
      attempt after a sent/unknown outcome. Concurrent requests, interrupted
      dispatch and a restarted producer retain this guarantee.
- [ ] Request state distinguishes a known result, a proven never-sent/refused
      attempt and an unresolved sent outcome. Missing provider usage/billing
      evidence remains explicitly unknown; provider/operator reconciliation
      evidence is request-specific, not inferred from a healthy status GET.
- [ ] ASR provider usage and any evidenced charge/cost are separately typed from
      Azure/Gemini **TTS monthly character counters**. TTS remaining characters
      must never be used as proof that transcription was charged or uncharged.
- [ ] Native local journal recovery validates authoritative request/body/result
      bindings and keeps unknown requests fail-closed. Existing held entries
      without authoritative reconciliation evidence stay held; no automatic
      `forget`, deletion, new-key bypass or fabricated confirmed answer.
- [ ] Ordinary and pilot contracts both have offline fault/security regressions;
      existing pilot attribution, speech budgets, provider/model selection,
      owner gates and journal protections remain effective.

## Steps

- [ ] Refresh main, all worktree/branch scopes and live remote/PR collisions before
      claiming implementation; coordinate the existing pretransport-admission
      and complete-answer journal tickets on shared native files.
- [ ] Define the ordinary request identity, durable dispatch/result/usage states,
      retention and caller authorization. A GET must not start or resend work.
- [ ] Preserve obtained provider usage with the result before returning it;
      integrate read-only request recovery with the normal client/journal.
- [ ] Add offline lost-answer, restart, concurrency, uncertainty and caller/body
      mismatch fixtures around the real native paths; document the recovery
      contract and the limits of historical requests without such an identity.

## How to verify

Use fake provider/HTTP transports and a disposable test database, never a paid
reproduction. Run the relevant focused suites after implementation:

```bash
node --test tools/video/tts/client.test.mjs tools/video/tts/speech-journal.test.mjs tools/video/tts/check-journal.test.mjs
cd apps/api && uv run pytest tests/test_video_speech_transcription_receipts.py tests/test_video_speech_check.py
```

Count provider dispatches separately from application POSTs and read-only GETs.
After one processed POST loses its response, restart both sides and recover the
same result and obtained ASR usage with zero additional provider dispatches.
When no authoritative result/usage exists, lookup must return unresolved and the
original journal must still refuse replay. Cover simultaneous same-ID requests,
changed body/locale/terms, wrong tool/user, lost provider response, failed durable
write, expired/unavailable evidence, and read-only lookup failures. Verify the
new web route with the existing speech route tests and normal task/API checks.

## Notes

- Filed only, **open and unclaimed**. No implementation, paid request, network
  action, journal mutation, settings change, approval or deployment occurred.
- Native evidence at filing: `tools/video/tts/client.mjs:32-38,199-227` only adds
  `operation_id`/`video_slug` for budgeted pilots; an ordinary body has neither.
  `schemas.py:141-153` returns `TranscribeOut{text}`. The ordinary branch in
  `admin_api.py:737-746` does not request `usage_out`; only the pilot branch
  collects/settles usage before `TranscribeOut` at 798-809. The underlying
  `checking.py` can collect `usageMetadata`, but ordinary callers do not persist
  or expose it per request.
- `GET speech/status` (`admin_api.py:444-471`) reports configuration, voices and
  TTS monthly character counters. HTTP 200/Gemini-ready is not evidence about
  whether the held ASR request executed or was billed.
- Existing done tickets for no-blind-retry, lost-answer proxy classification,
  and check-audio journals protect uncertainty; they do not implement ordinary
  server-side result/usage retrieval. Open
  `2026-10-09-video-speech-pretransport-admission` concerns proof of zero paid
  dispatch before admission failure. Open
  `2026-10-09-recover-own-complete-speech-answers-after` concerns a complete local
  staged answer after a Windows promotion refusal. Neither is this sent POST
  with no answer. Pilot budget receipts are not applicable to ordinary ForTy.
- Offline duplicate check covered open/done files, including uncommitted files,
  in all five current worktrees and task trees of all six local branches. No
  same ordinary-ASR durable recovery ticket was found. Two cached origin refs
  and local `origin/main` history were inspected; live remote heads/PRs were
  deliberately not queried under the no-network filing instruction. Refresh
  those checks before implementation, rather than treating this as a live PR
  clearance.
- Scope lists exact native files and proposed new receipt/model/test/GET files,
  not whole apps/tool directories. The proposed migration filename is a narrow
  placeholder: before implementation, verify the actual current Alembic head
  and update that one scope entry/name if needed; do not reserve a stale numeric
  revision or create a second head. No migration/model file is created here.
- Original ES held journal, source WAVs, M4A/fit/meter and cached transcript
  evidence remain in the producer's immutable external archive. Changing hints,
  model, locale or request body to evade that held fingerprint is not recovery.
