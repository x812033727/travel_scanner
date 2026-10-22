---
id: 2026-10-22-guard-c07-dr-martens-paid-pilot
title: Guard C07 Dr Martens paid pilot by episode budget
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-10-22T15:10:44Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_budget
  - apps/api/migrations/versions
  - apps/api/tests/test_video_pilot_budget.py
  - tools/video/tts
  - tools/video/media
---

# Guard C07 Dr Martens paid pilot by episode budget

## Why

C07's script/visual direction is owner-approved and its nonpaid whole-film quote proposes at most 86 images, 258 image/judge attempts, 73 TTS lines, one music track, and a USD 25 hard stop. On 2026-10-22, C07 is absent from the server `video_budget` pilot slug set and local media/TTS pilot slug sets. Paid calls would therefore bypass per-episode attribution and could violate the hard stop. This task must be completed before asking the owner for C07 paid-pilot authorization or sending any paid request.

## Definition of done

- [ ] The exact C07 slug uses one attributed USD 25 account across TTS/ASR, image generation, image judging, music, retries, ambiguous provider outcomes, and local/host routes.
- [ ] New accounts start with no historical spend only after read-only evidence confirms no C07 paid calls; otherwise reserve uncertainty first. No fresh spendable USD 25 is created atop prior exposure.
- [ ] Host migration, deployed code, operation ledger and remaining-USD readback prove the limit before STOP is removed or a request is sent.

## Steps

- [ ] Coordinate with active C03–C06 budget guard/reconciliation and migration/TTS scope holders; do not claim overlapping scopes until released.
- [ ] Inspect current deployed budget model and migration head; add C07 account/slug and exact client attribution with stable operation IDs, including auditions and retry handling.
- [ ] Add targeted tests for missing account, ambiguous response, duplicate operation, full cap, and all paid media routes.
- [ ] Verify PostgreSQL migration upgrade/repeat, deployment and account/operation readback. Keep C07 paid STOP until owner approves the exact production quote and all gates pass.

## How to verify

Targeted API budget/migration integration tests, TTS and media client tests, `npm run check:tasks`, then host readback of the C07 account and ledger. The quote and approved artifact hashes are in `docs/videos/story-everyday-dr-martens-c07/production-quote.md` and `reviews/owner-script-approval.md` on draft PR #1680.

## Notes

No paid C07 generation is known as of this ticket; verify rather than assume zero. C03–C06 each have separate unresolved historical costs and STOP files; do not share or transfer their balances. PR #1684 is a partial C03–C06 guard, not C07 coverage. Script approval is not cost approval, and this ticket alone authorizes neither paid calls nor upload/publication.
