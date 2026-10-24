---
id: 2026-10-24-preflight-required-sfx-before-paid-dub
title: Preflight required sound effects before paid dub speech
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-24T13:26:50Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/dubs/cli.mjs
  - tools/video/dubs/dubs.test.mjs
---

# Preflight required sound effects before paid dub speech

## Why

Independent review found required SFX are validated by sfxInputs inside dubSound only after paid synthesize. Missing or hash-stale SFX can spend narration before failing. This is separate from the completed music preflight.

## Definition of done

- [ ] Malformed/missing/hash-stale required SFX refuse before speech status/synthesis, creating no new cache or journal.
- [ ] Existing paid history remains; mix-time validation still catches a later race.
- [ ] Focused regressions and independent duration binding pass.

## Steps

- [ ] Recheck active scope and claim the ticket before editing.
- [ ] Reproduce failure with fake provider, then apply a narrow preflight and retain negative cases.

## How to verify

Run the scoped dubs suite, full tools checks, independent long-form receipt check and task validation. No actual provider request is needed.

## Notes

Found in2026-10-24 independent review: dubs/cli.mjs sfxInputs inside dubSound, paid synthesize before that call; assemble/sound.mjs performs manifest/file/SHA validation. Preserve retained media/provider receipts. No production or paid action authorized by this ticket.
