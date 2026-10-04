---
id: 2026-10-04-prevent-paid-speech-retries-after-ambiguous
title: Prevent paid speech retries after ambiguous transport outcomes
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-04T15:41:30Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
---

# Prevent paid speech retries after ambiguous transport outcomes

## Why

The shared speech client retries a thrown fetch error and general 5xx responses inside `call`, with five attempts by default. For paid synthesis, transcription or judge POSTs, the server may have completed work before the connection lost its answer. Unlike the automation run client, this path does not distinguish a request never sent from an uncertain paid outcome. A retry can therefore pay for the same input again. This was found by source inspection during AI-series production; no duplicate charge is claimed.

## Definition of done

- [ ] A paid request whose outcome is unknown stops and records enough input identity to reconcile; it is never blindly resent.
- [ ] Definitive never-sent or server-settled failures retain the intended bounded recovery, and read-only status GETs can still retry.
- [ ] Returned WAV/transcript/judge results and actual billed usage remain bound to their request; existing current caches are reused without forged evidence.

## Steps

- [ ] Audit all shared POST callers and classify network errors, gateway errors, incomplete response bodies and settled provider failures.
- [ ] Add source-bound reconciliation/recovery without changing provider, model, voice, budget or approvals.
- [ ] Cover lost-after-send and lost-response-body cases with fake transport tests that assert one paid submission.

## How to verify

Run `node --test tools/video/tts/client.test.mjs` and relevant synthesis/audio callers. Use fake transports to prove ambiguous outcomes submit only once while safe failures and GETs retain their allowed recovery. Do not reproduce the failure against a paid provider.

## Notes

- `tools/video/tts/client.mjs:39` retries fetch exceptions; defaults at68 use five attempts. `synthesize` at103 sends the paid POST through that helper, then reads the WAV body. Shorts' `serverNarration` writes its cache only after a returned synthesis result.
- Existing `tools/video/automation/client.mjs` distinguishes never-sent and uncertain model runs; do not assume that protection already covers speech.
- The LLM episode's narration is complete and reused; no synthesis or paid retry was started after this finding. The current task leaves shared client files unchanged.
