---
id: 2026-10-09-recover-own-complete-speech-answers-after
title: Recover own complete speech answers after Windows journal promotion refusal
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-09T18:41:38Z
completed_at:
branch: codex/stalled-video-reviewed-fixes-20261008
depends_on: []
scope:
  - tools/video/tts/speech-journal.mjs
  - tools/video/tts/speech-journal.test.mjs
---

# Recover own complete speech answers after Windows journal promotion refusal

## Why

Embedding received a complete ASR HTTP200 response and fsynced its exact
generation-bound staged answer,but final Windows canonical journal rename
still failed after10230ms. The normal caller stopped before saving this answer
to its check cache. The complete response must remain reusable without a second
provider request or a fabricated canonical confirmation.

## Definition of done

- [ ] A current producer can return its actual completed response after a final
      Windows rename refusal only after strict stage/body/generation validation
      and immutable archive preservation.
- [ ] Interruption before cache/release still permits normal closed-producer
      recovery with zero provider requests.
- [ ] Unknown responses,foreign live producers,evidence drift and unrelated
      I/O errors retain the ordinary holds; release protects newer generations.

## Steps

- [ ] Review current main/PR1379 against the private9d8dccaa journal delta.
- [ ] Adopt the narrow persistence behavior with meaningful native fault and
      interruption fixtures; preserve original provider/correction/owner gates.

## How to verify

Use a genuine normal journal with an injected final canonical rename refusal.
Check SENT plus complete fsynced stage and immutable archive before handout.
Run a real child that exits before caller cache/release,then recover normally
with sender0. Verify refusal for wrong body/hash/generation,missing stage,
foreign live producer,wrong rename destination/non-rename/I/O/archive errors.
Check normal release cannot remove an unrelated/newer unknown generation.

## Notes

The private generation-bound fallback was used without retransmitting the
complete known answer. Final native result35fb8670 retains three genuine SKIPs
and all1323 speech/nine model transports; no manual canonical confirmation,
QA clearance or extra round is inferred. Product-code adoption of the scoped
speech-journal primitive remains unimplemented and unclaimed.


- Operational source,fixtures and receipts are outside Git under
  `<home>/mokaair-work/stalled-video-completion-20261008/embedding-audio/listener-round2/selected-language-finishing-20261009`.
- Private source9d8dccaa and original-URL loaderc1fff337 passed root and
  independent15/15 actual offline fixtures. This is source evidence; repository
  adoption and production outcome are separate.
- The first67dd candidate wrote current-producer context into the ordinary
  proof.json and broke subsequent closed recovery. Never adopt that version.
  Version9d8 uses separate immutable current-producer-proof.json,keeping the
  ordinary closed proof.json byte compatible. A real interrupted-child test
  proves this fixes the restart blocker with no additional sender call.
- Exact9cd closed-answer proof19368c1e reused its actual response through the
  normal journal with sender0 in an owned copy. All177 originals are archived;
  current canonical/cache remained unchanged. Preserve both historical SENTs.
- Production locking cause remains unproved. This ticket does not authorize
  provider retries,QA changes,owner approval,uploads or deployment.
