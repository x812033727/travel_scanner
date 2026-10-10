---
id: 2026-10-09-video-speech-pretransport-admission
title: Distinguish admission read failures from dispatched paid speech requests
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-09T12:01:39Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/client.mjs
  - tools/video/tts/speech-journal.mjs
  - tools/video/tts/speech-journal.test.mjs
  - tasks/open/2026-10-09-video-speech-pretransport-admission.md
---

# Distinguish admission read failures from dispatched paid speech requests

## Why

The normal speech journal marks a request sent before its wrapped transport
function executes. A source/owner/settings admission GET inside that function
can fail before any paid HTTP request. On 2026-10-09 the FREE Japanese continuation
was held as video_speech_uncertain after a reviews GET429, although the frozen
transport branch and its complete wire log prove the speech network was never
invoked. The owner-facing message incorrectly says the POST was sent and might
have been charged. Genuine uncertain paid requests must still remain protected.

## Definition of done

- [ ] Proven failures before paid transport are distinguishable from requests
      that entered the paid transport and lost their response.
- [ ] A temporary admission GET429 can wait within a bounded interval while
      owner/source/STOP guards remain effective; mutations are never retried.
- [ ] Genuine sent/unknown journals retain their existing no-replay semantics.

## Steps

- [x] Reproduce the actual pretransport failure with the pinned normal native
      client and journal, without provider or production API calls.
- [ ] Implement and review an explicit admission/dispatch boundary in the normal
      speech path without changing paid request identity or cost limits.
- [ ] Verify source/owner/STOP changes, GET429, network failure after dispatch,
      restart and retained-journal cases with meaningful regression tests.

## How to verify

Run the focused native speech client/journal tests and the applicable tools
checks. Tests must count actual paid transport invocations, including zero
invocations for rejected admission, and must prevent a restart from replaying a
genuinely sent unknown request.

## Notes

Additional Oct10 postproduction diagnosis: admission metadata persistence can
also fail before any normal transport. Actual SH5 v2 receipt-rename refusal
d4e7dcd1 retains the old/temp raw read, four absent processes and zero LANG
intents/returns/POST/PUT. Three private relay sources retry only the same
fsynced receipt rename on EPERM/EBUSY, without a new SQL timestamp or API call;
23 focused cases pass. This private operational repair does not implement the
normal paid admission/dispatch boundary. Genuine sent/unknown holds remain.


Actual retained operation44a0a83921d0fc12a5f0365aa17e55d211e4df402ef61bdbe69d351c504e674e
has held journalc8070fa5535d9294ef150525c858d128d9a123c8c74b35f457e950b5e8329943.
Its sent-to-held interval is106ms and its reason is the reviews admission GET429.
The preceding38 speech POSTs all returned HTTP200; the complete wire contains no
transport with that request hash. The matching private proof is
selected-dub-44a-pretransport-evidence-readonly.json,
SHAe169a69e665ab8437bc09392e0efe99e8119dd6fcf63c92f50c18a6c82705740,
under C:/Users/x8120/mokaair-work/handoff/branding-peak-20261008/continuation.
Nine private negative tests use frozen transportcd641633, native client75af667e
and journalf60191ff; they reproduce the held result with zero paid network calls
and verify that restarting it also sends nothing. They are diagnostic fixtures,
not an installed repository fix or authority to clear arbitrary held journals.
The original Korean unknown operation and Mods hold remain untouched. This task
is released after recording evidence; guarded video delivery remains ongoing.

Additional actual recovery examples on October9:

- DevDay request d430 stopped on the deploy flock before the wrapped wire
  logger/network. Exact proof1583d812 records zero dispatches and190 earlier
  HTTP200 responses. Normal exact-key reconciliation receipt9d4f3dc8 archived
  all457 entries first and retained the other456 plus four confirmed answers.
  This operational recovery made zero provider/API calls; it is not a shared
  client/journal implementation fix.
- Embedding's next request e36 stopped on the15-second actual snapshot guard,
  also before the wire logger/network. Proof f98e941d retains the precise body,
  held journal,closed producer and zero matching transport,plus all11 successful
  responses/985 characters,14 new WAVs and original fourteen journals. Private
  evidence is under `<home>/mokaair-work/stalled-video-completion-20261008/`
  `embedding-audio/listener-round2/selected-language-finishing-20261009`.
- A separate remote reader whose stdout is processed by the paid parent still
  cannot refresh its local receipt during synchronous synthesis/hash work.
  Receiver independence must be tested with an actual parent stall longer than
  the freshness interval. The recovery must keep original completed-read times
  and dispatch boundaries; extending freshness or clearing arbitrary held keys
  does not resolve the underlying distinction.

Both examples retain original counters,approved media and actual paid history.
The genuine old FREE unknown and Mods STOP remain unchanged. This note records
diagnosis only; the shared implementation remains open.

Current35 recovery also reproduced the same distinction for Travel ASR b3ab:
closed caller137 retains82 synthesis/94 ASR results, while full original wire
af81c5fa contains no transport for the exact full native transcribeBody key.
Normal exact-key reconciliation receipt7d4af1c1 archives the raw request first;
the genuine next ASR returned200 without resetting cached checks or rounds.

Future admission hardening should reject invalid or excessively future read
times and separately validate the host-check age. Private source-only advice
d4349e4a records the same-host guards and original source hashes. No future
timestamp was observed at that historical admission snapshot. This remains a
diagnostic follow-up, not authority to replay genuine unknown requests or
extend read freshness.

A later SH6 Tail zero-write dry retained22 genuine host checks. Its last host
timestamp was71ms later than native finish while SQL age was332.867ms; the
exact guard instant was not logged, so the precise failing host age is unknown.
The original v1 dry returned3, all four actual processes closed, auto remained
unchanged and no native/progress intent was created. The interrupted v2 dry
retains UNKNOWN original true exit and zero writes, without a success claim.
The v3 readiness refusal returned3 before any native spawn; its three actual
processes closed. Successful v4 dry returned native/coordinator true0 with
four actual processes closed; the one actual v4 execute then returned true0
and one ordinary progress PUT200. These preserved purposes were never replayed.

The private clock helper waits at most five seconds per original completed read
using actual local time, without restamping SQL/host evidence. It preserves the
original native0..60-second and readiness0..15-second age checks plus the original
120-second readiness deadline. Native16 focused cases and readiness10 cases pass.
This private bounded wait is not a repository admission/dispatch implementation
fix. Genuine sent/unknown paid holds remain protected; this task remains open
and unclaimed, with no blind retry authority.
