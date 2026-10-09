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
