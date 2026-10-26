---
id: 2026-10-26-recover-ordinary-tts-receipts
title: Recover ordinary TTS results and usage after lost POST answers
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-26T07:12:53Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/client.mjs
  - tools/video/tts/speech-journal.mjs
  - apps/api/app/video_speech/admin_api.py
  - apps/api/app/video_speech/schemas.py
  - apps/api/app/video_speech/azure.py
  - apps/api/app/video_speech/gemini.py
  - apps/web/app/api/video/speech/forward.ts
  - apps/web/app/api/video/speech/route.ts
---

# Recover ordinary TTS results and usage after lost POST answers

## Why

An ordinary, non-pilot `POST /api/video/speech` can lose its usable answer after
dispatch. The native client correctly retains that exact request as held instead
of blindly buying it again. The normal contract currently has no durable,
request-specific TTS dispatch/completion/result/usage lookup, so neither a later
healthy `speech/status` GET nor monthly character counters can resolve its
possible charge or retrieve a completed WAV.

On 2026-10-26, one authorized native PT retake process for `forty-forest-map`
ran from 06:50:04.672 to 06:50:36.418 UTC, PID 258624, and actually exited 3.
The final send was recorded at 06:50:35.612Z and held at 06:50:36.182Z with
`no usable answer came back (HTTP 502)`. The exact local sent-body SHA256 is
`3cc1ce6b7a4c1026cc52686be17962a255277ad86f795c46c88378068c0ee456`;
the held journal SHA256 is
`b9d12c0e77dc02ec913bf8f23b82089e5172ae93675b24f39dea14a31203f75d`.
That body fingerprint is not a server/provider request ID. The 502 is observed
at the Mokaair-facing boundary without a usable error code; its origin layer,
provider response, dispatch/completion and charge are unknown.

All 92 local source-WAV hashes remained unchanged, no new native stage completed,
and no same-request complete/staged answer was found. Zero changed local WAVs
does **not** mean zero provider charges or that the other four intended retakes
succeeded. One native process does not establish the count of HTTP POSTs or
provider dispatches. The original held journal, retake/shortening/reword limits,
and separate unresolved ES transcription receipts remain intact. This task
does not authorize their replay, deletion or fabricated confirmation.

Preserved evidence in the producer's external `work/ai-tech-next` directory:

- `forty-pt-branded-R1-once.v3.result.json`, SHA256
  `270e87da89dcda63898f8ac657294eca7645dba6ad76f1d5e6955163386c7e62`.
- `forty-pt-branded-R1-v3.root-unknown-outcome-review.json`, SHA256
  `bdd5318d339910e8428f18bc32833bdf8b7f49e90312b1bb9d91b014e4787648`.
- `forty-pt-uncertain-speech-capability.readonly.json`, SHA256
  `ce70760f658183e41df812bf22b595bd8a1de0557310a1326093b8489dd2a552`.

These are source/metadata and actual-process receipts, not evidence of a charge,
no charge, recovered audio, implemented recovery endpoint or deployment.

## Definition of done

- [ ] Ordinary TTS has a durable caller-authorized logical request identity,
      bound to exact sent body, voice/model/style, and obtained audio/usage.
      A documented normal read-only lookup reports dispatch, completion,
      unresolved outcome, retained result and any evidenced charge without
      starting or resending work; recovery survives API/client restarts.
- [ ] Reuse of the same identity cannot dispatch another paid provider attempt
      after sent/unknown outcome. Concurrent callers, failed persistence and
      interrupted dispatch preserve that guarantee; changed input or another
      caller cannot reuse or read this request's result.
- [ ] A complete obtained WAV and provider usage/receipt are durably preserved
      before returning success. Audio receipt/completion, provider usage,
      evidenced charge and current-audio acceptance remain separate facts.
      Missing provider evidence is explicitly unknown, not zero or no charge.
- [ ] Normal lookup and journal recovery validate authoritative caller/body/
      result bindings. Historical held entries lacking those records stay
      held, including this PT request and the separate ES holds; no automatic
      forget/delete, new-body/key bypass, fabricated confirmed journal or usage.
- [ ] Current native budgets, retake/shorten/reword caps, caches, source/owner
      gates and unknown-result retention remain effective. Normal existing
      authentication, UA, TLS and proxy rules remain intact; no provider keys,
      tokens, request text or credential-bearing URLs enter logs or receipts.
- [ ] Request-specific provider/operator reconciliation can retain genuine
      dispatch/completion/billing evidence without inferring it from aggregate
      monthly counters, healthy GETs, elapsed time, HTTP502 or absent local WAVs.
      Any unavailable evidence keeps the request unresolved and unreplayed.
- [ ] Focused offline restart, concurrency, lost-answer, wrong-caller/body,
      evidence-drift and failure fixtures prove zero extra provider dispatches
      during GET/recovery. Existing ordinary and pilot behavior remains covered.

## Steps

- [ ] Refresh main, worktrees, remote branches, open PRs and active scopes before
      claiming implementation. Coordinate the related ordinary-ASR receipt and
      speech-journal/promotion owners; do not take over or widen another task.
- [ ] Define the ordinary TTS identity, durable dispatch/result/usage states,
      retention, exact caller authorization and reconciliation evidence. Choose
      actual storage/migration/GET/test paths only after that design; expand
      this initial boundary-only scope with collision review before writing
      any additional file, rather than treating hypothetical endpoints as real.
- [ ] Persist obtained audio/usage before response, add the documented normal
      zero-dispatch read contract, and integrate strict native client/journal
      recovery without changing paid input, provider, caps or approvals.
- [ ] Add fake-provider/disposable-storage regressions around the real native
      paths; document which future requests are recoverable and why this
      historical request remains held without authoritative reconciliation.

## How to verify

Use fake HTTP/provider transports and disposable storage/database fixtures,
never a paid reproduction. After one processed POST loses its HTTP answer,
restart both sides and recover the same WAV and obtained usage by the documented
normal authorized GET with **zero additional provider dispatches**. Count
application POSTs, provider dispatches and read-only GETs separately.

If the provider answer or durable receipt never arrived, GET must return
unresolved and the original journal must still refuse replay. Cover simultaneous
same-identity requests, changed voice/model/style/body, wrong tool/user, partial
WAVs, stale or missing evidence, failed durable writes, interrupted dispatch and
read failures. GET must never issue a paid POST. No fixture may manufacture
provider usage, clear flags/holds, or turn receipt/completion into ASR acceptance.

Run the existing focused suites plus the actual new receipt/security suite
selected after scope expansion, and the normal task checker:

```sh
node --test tools/video/tts/client.test.mjs tools/video/tts/speech-journal.test.mjs
cd apps/api && uv run pytest tests/test_video_speech.py tests/test_video_speech_gemini.py
```

From the repository root, run `npm run check:tasks`; verify the normal web speech
route suite after implementation. This filing has run task-format checks only,
not implementation tests, production requests or provider reconciliation.

## Notes

- Filed **open and unclaimed** only. No implementation, shared source change,
  API/auth/provider request, paid work, journal mutation, cap reset, setting,
  approval, merge or deployment is part of filing this task.
- Related but different: [ordinary transcription receipts](2026-10-26-recover-ordinary-transcription-receipts.md)
  covers ES ASR result/usage. This task covers ordinary TTS/WAV/charge recovery;
  coordinate shared boundaries without claiming either planned capability is
  already available. [Local complete-answer promotion recovery](2026-10-09-recover-own-complete-speech-answers-after.md)
  requires a genuinely retained answer and does not resolve this held request.
- Native evidence at filing: `speech/status` is the only speech business GET
  (`admin_api.py:444-471`) and returns configuration plus monthly TTS counters.
  The normal client says the server retains no answer/idempotency key
  (`client.mjs:32-38`); ordinary non-pilot calls do not get the pilot operation
  UUID (`199-208`). ForTy is not a budgeted story pilot. Pilot host-only ledger
  inspection is not a normal tool-token request lookup or WAV retrieval.
- Gemini/Azure handlers return the current WAV response with
  `X-Billable-Characters` and `Cache-Control:no-store`; ordinary Gemini drops
  the obtained usage metadata. The monthly Redis counter has no request-SHA
  row. Source inspection is not proof of deployed server revision or billing.
- The journal only attempts retained complete-answer recovery for canonical
  `sent`; canonical `held` refuses (`speech-journal.mjs:405-413`). This PT entry
  is held and has no adjacent saved/staged answer. Do not rerun native synthesis
  to investigate, invoke forget, hand-edit confirmed/sent, copy another take,
  generate a changed body to bypass the hold, or reset a budget/cap.
- Filing collision check on `codex/ai-tech-forty-20261025` at
  `979cfd60468f0685d5447b8011a95ab2bb51a0f0` found no matching ordinary-TTS
  task and no nonstale local overlapping claim. The broad
  `2026-10-19-worker-video-languages-five` review claim overlaps these native
  files and is marked stale since its 2026-10-20 claim; its owner/task were
  untouched. Local worktrees/branches were inspected, but no remote/PR API
  lookup was made in this bounded filing. Future implementation must refresh
  all collision/main/PR evidence before claim; filing grants no takeover.
- Initial scope lists only eight existing, SHA-verified native boundary paths
  from the read-only research. It does not preselect nonexistent durable model,
  migration, endpoint or test files. Those require the explicit scope refresh
  in Steps before implementation; do not implement a partial non-durable fix
  merely to stay within the initial list.
- A future durable contract cannot retroactively prove execution, charges or
  audio for this historical 502. Missing request-specific authoritative evidence
  remains a production hold. No unrelated project, page, schedule, global
  pipeline setting or existing pending-narration progress ticket is in scope.
