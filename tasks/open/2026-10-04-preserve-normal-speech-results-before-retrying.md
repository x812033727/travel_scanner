---
id: 2026-10-04-preserve-normal-speech-results-before-retrying
title: Preserve normal speech results before retrying uncertain paid requests
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-04T13:06:25Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
---

# Preserve normal speech results before retrying uncertain paid requests

## Why

The shared native speech client defaults to five attempts for a synchronous paid
POST. Losing a response can repeat synthesis, transcription or audio judgment
after the first server operation has already completed. Normal videos still use
that client behavior. The isolated approved-final language runner now has a
source-bound fetch journal, but that protection is scoped to its six current
sources and must not be reported as a general speech-client fix.

## Definition of done

- [ ] A lost paid POST or response body cannot trigger another paid dispatch in
  the normal client; safe GET retries and owner/quota classification still work.
- [ ] Confirmed complete response bytes can be consumed without being bought
  again; unresolved results remain a visible hold rather than fake success.
- [ ] Preserve current source, voice, model and budget authority and never infer
  listening acceptance from an HTTP response or local audio check.

## Steps

- [ ] Choose a result-preserving contract before extending beyond the current
  batch journal; inspect real native consumers and current backend capabilities.
- [ ] Exercise real synthesize/transcribe/judge consumers with lost POST, lost
  body, corrupt result, changed request and restart fixtures.

## How to verify

Use an injected counting fetch with the actual native client. A dropped paid
response must submit once, not five times. Verify owner and exhausted-budget
errors retain their existing meaning and no test calls a live paid endpoint.
Run the affected tools tests and the repository tools suite.

## Notes

- Found during the 2026-10-04 video recovery. The existing call loop is in
  tools/video/tts/client.mjs; default attempts are five and network/429/5xx retry.
- docs/videos/imported-long-languages/speech-journal.mjs is a reviewed local
  reference with raw WAV/JSON preservation and unknown-result holds. Its 54
  native-consumer regressions passed independently; do not simply enable that
  source-specific contract for unrelated projects or weaken existing gates.
- This is an unclaimed follow-up, not completed or deployed work. Expand scope
  only after checking active claims if integration requires other files.
