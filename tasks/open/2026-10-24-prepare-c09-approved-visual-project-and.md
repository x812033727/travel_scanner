---
id: 2026-10-24-prepare-c09-approved-visual-project-and
title: Prepare C09 approved visual project and paid pilot quote
status: in-progress
priority: P1
area: docs
owner: codex-c09-v8-promotion
claimed_at: 2026-10-24T06:16:37Z
created_at: 2026-10-24T06:11:26Z
completed_at:
branch: codex/c09-patagonia-script-repair-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-patagonia-c09/visual-plan.md
  - docs/videos/story-everyday-patagonia-c09/visual-plan.json
  - docs/videos/story-everyday-patagonia-c09/reviews/visual-plan-v5-85-historical.md
  - docs/videos/story-everyday-patagonia-c09/series.json
  - docs/videos/story-everyday-patagonia-c09/brief.md
  - docs/videos/story-everyday-patagonia-c09/preflight-v8.mjs
  - docs/videos/story-everyday-patagonia-c09/video.json
  - docs/videos/story-everyday-patagonia-c09/production-quote.md
  - docs/videos/story-everyday-patagonia-c09/pilot-readiness.md
---

# Prepare C09 approved visual project and paid pilot quote

## Why

Owner approved C09 v8's 77 narration lines and 77 matched visual directions,
but the current canonical `visual-plan.md` still has 85 old rows and there is
no frozen `video.json`. The paper 567.633-second body is not a TTS result.
Keep the exact reviewed direction together before anyone begins paid media.

## Definition of done

- [x] Canonical visual plan and `video.json` have exactly the approved 77
      IDs, narration texts and matched visual directions, with a verified
      mapping to the frozen v8 candidate SHA-256. Only ten postproduction
      card title/source strings and four pronunciation-only `say` fields differ.
- [x] Textual visual preflight and local lint pass, with all exceptions and
      measured-versus-paper timing states recorded.
- [ ] Whole-film quote specifies image/voice/review/music quantities and
      a hard all-in US$25 stop for owner consideration; it does not treat
      C09 script approval as paid authorization.

## Steps

- [x] Claim the narrow paths after checking branch and task-board ownership;
      reuse the shared checkout, never create a full repo copy for review.
- [x] Start from `reviews/visual-plan-v8-candidate-2235ea30.json` SHA-256
      `2235EA304C240E78F6473183E45A63502500EE20F931107843C6AF3C5AD0BF5A`;
      preserve the 77/77 independent source/visual PASS and both blind reads.
- [ ] Guard against stale regeneration from the old 85-line project and run
      local `lint` plus safe dry-run checks. Do not run paid APIs or worker.
- [ ] Price the complete pilot, inspect single-episode budget routing and
      prior spend, then ask for separate owner paid approval only after a
      concrete, independently checked quote.

## How to verify

Compare the candidate and canonical 77 IDs/texts/prompts programmatically;
run `node tools/video/cli.mjs lint --slug story-everyday-patagonia-c09` only
after `video.json` exists; run `npm run check:tasks` and `git diff --check`.
Actual voice WAV durations must show body >=480 seconds before buying images.

## Notes

PR #1806 stays draft/no-auto-merge. Canonical `script.md` now equals the
owner-approved v8 candidate hash `4445AD74BCAFBAC1DFCA65392199FEC89700C17AB8C01E665AC79DFFFC1AA3F7`.
Approval receipt is `reviews/owner-v8-approval-20261024.md`. Signed blind A
is 11/12 Yes (`natural_spoken=No` at c090302/c090401/c090418), B 12/12
Yes; no common veto. No C09 paid approval, import, upload, or publication.

The current local project was generated with
`preflight-v8.mjs` and independently checked: 77/77 scene and narration
alignment, 67/67 shot data unchanged; 10/10 card values and labels unchanged.
Only the visible card title/source captions were made viewer-facing, retaining
the frozen candidate separately. Project SHA-256
`4ABEBBF0936CD77269A55F197B7051534EE5140785929C9287A13CAE122AD460`.
Video lint: 0 errors, 10 warnings. See `pilot-readiness.md` for holds. The
whole-film quote and budget route remain unfinished, so this ticket stays
in-progress. The generic worker guard has a separate unclaimed task
`2026-10-24-guard-c09-v8-stale-worker`, because the core path has other
claims; no force claim was used.
