---
id: 2026-10-20-produce-target-x08-narration-and-validate
title: Produce Target X08 narration and validate timing
status: in-progress
priority: P1
area: docs
owner: codex-x08-media
claimed_at: 2026-10-20T18:03:31Z
created_at: 2026-10-20T18:03:29Z
completed_at:
branch: codex/brand-story-target-x08
depends_on: []
scope:
  - docs/videos/story-everyday-target-x08/drafts/narration.md
  - docs/videos/story-everyday-target-x08/drafts/visual-cues.mjs
  - docs/videos/story-everyday-target-x08/compose-video.mjs
  - docs/videos/story-everyday-target-x08/video.json
  - docs/videos/story-everyday-target-x08/script.md
  - docs/videos/story-everyday-target-x08/line-source-matrix.md
  - docs/videos/story-everyday-target-x08/source-matrix.md
  - docs/videos/story-everyday-target-x08/source-notes.md
  - docs/videos/story-everyday-target-x08/README.md
  - docs/videos/story-everyday-target-x08/treatment.md
  - docs/videos/story-everyday-target-x08/visual-plan.md
  - docs/videos/story-everyday-target-x08/publishing-handoff.md
  - docs/videos/story-everyday-target-x08/reviews/source-audit-v6.md
  - docs/videos/story-everyday-target-x08/reviews/blind-a-v6.md
  - docs/videos/story-everyday-target-x08/reviews/blind-b-v6.md
  - docs/videos/story-everyday-target-x08/reviews/media-production.md
  - docs/videos/story-everyday-target-x08/reviews/blind-a-v7.md
  - docs/videos/story-everyday-target-x08/reviews/blind-a-v9.md
  - docs/videos/story-everyday-target-x08/reviews/blind-b-v9.md
  - docs/videos/story-everyday-target-x08/reviews/source-audit-v7-independent.md
  - docs/videos/story-everyday-target-x08/reviews/source-audit-v8-visual.md
  - docs/videos/story-everyday-target-x08/reviews/source-audit-v9-delta.md
  - docs/videos/story-everyday-target-x08/reviews/v10-author-delta.md
  - docs/videos/story-everyday-target-x08/production-quote.md
  - tasks/open/2026-10-20-produce-target-x08-narration-and-validate.md
---

# Produce Target X08 narration and validate timing

## Why

X08 Target Canada has a source- and narration-reviewed offline script plus a pinned pronunciation lexicon, but no real Sulafat audio or measured timeline. The owner's style requires a 30–60-second condensed opening and at least eight minutes of substantive body narration, and future image/ASR/Shorts/music/QA must fit the same US$25 all-in cap. This ticket produces and checks the local narration before any image batch or claim of a finished film.

## Definition of done

- [ ] The exact pinned X08 script has current Sulafat audio and a measured timeline; serial transcript/listening QA is complete or any remaining flagged lines are recorded as a hold.
- [ ] Opening and substantive body are measured against the 30–60-second and 8-minute requirements, with a source-safe remedy if either fails.
- [ ] The media ledger and remaining work are accounted against the US$25 hard cap. No art batch starts until current image/judge quota and all-in cost can cover the whole 113-shot plan; official brand assets, final cut and Studio links are separate gates.

## Steps

- [x] Create narrow scoped ticket after the reviewed manual lexicon bootstrap was committed to draft PR #1625.
- [x] Run first pinned Sulafat TTS (130 requests / 2,643 actual billable characters), with the paired tool; preserve actual clips and timeline hashes. Stable-ID v6 has ten new lines still to synthesize.
- [ ] Run serial `check-audio` and resolve or explicitly hold real discrepancies without inventing new source claims.
- [ ] Measure first chapter and substantive body from actual audio; document exact frame/time evidence and update the all-in budget gate.
- [ ] If spoken body is shorter than eight minutes, add source-backed story material, rebuild and obtain new exact-SHA source plus two blind reviews before incremental TTS.
- [ ] Commit/push an honest X08 media receipt to draft PR #1625; keep future production dependencies explicit.

## How to verify

Use X08 worktree `/workspace/travel_scanner_target_x08`, work base `/workspace/.brand-video-workdir`, and paired credential home `/workspace/.video-tool-home` with `NODE_USE_ENV_PROXY=1`; never copy tokens to the repository. Run `node tools/video/cli.mjs lint --file docs/videos/story-everyday-target-x08/video.json --json`; `tts --slug story-everyday-target-x08 --workdir /workspace/.brand-video-workdir` via the tool's exported `main(..., {home})`; then `check-audio` serially with the same work base. Inspect `timeline.json`, `narration.wav`, each line's check results, media ledger, and run `npm run check:tasks` plus `git diff --check`. Strict body timing excludes opening, 5-second intro, 21-second outro, CTA, silence and artificially slowed speech.

## Notes

- Manual lexicon bootstrap is already committed on #1625 as commit `3d3b90f8`, with immutable version `ec1cafa975b5bd7a4085862ec1a7b6759206859f6a8948f58f89aafc6cca41b3`; `/root` independently verified strict readback and no prior audio.
- Pinned paired TTS dry-run returned **130 requests, 2,602 billable characters**, `gemini:Sulafat` ready and 8,563,008 monthly Gemini characters remaining. This is a free-tier capacity check, not a measured duration or new media charge.
- Prior source-frozen `video.json` SHA-256 `a6ffe45d1944839e0ae35c9e8418e340dacef578e7faa5304219b80fe4118bb4`; `shorts.json` `440ceee9649b30af2bd64ff1205bf38bff47d0be381b1b544cccff4601e2d543`. New stable-ID video SHA is `7919666e43bc77f6e27d3c4d566c46bd6b77f17e675547d9e62f6ce6febcb0b8`: source-audit-v6 PASS, blind A/B pending. The original 134 scenes/lines are byte-equivalent in content and IDs, and Shorts SHA is unchanged.
- First actual TTS finished: 130 requests / 2,643 billable characters, 134 WAVs and `narration.wav` 624.8 seconds. Opening spoken 36.17 seconds meets 30–60; substantive body spoken 441.94 seconds, so the eight-minute gate **fails** despite 561.83 seconds including scene gaps. Parent authorized a sourced 45–55 second Chapter 3 extension, new exact-SHA source and blind receipts, then incremental TTS. The paired tool's untracked `node_modules` symlink must not enter Git.
- Independent FY2013 10-K source audit for the ten new REDcard/store-area lines and new native comparison card is PASS. Lint for stable-ID v6 is 0 errors/0 warnings, 144 lines, 122 shots, 15 cards and 16 loops. Paired TTS dry-run sees exactly **10 pending requests / about 269 characters**; all 134 original WAVs are reusable. New audio/strict duration and serial check-audio wait for the two v6 blind receipts. Shared image/judge quota is reserved for other episodes; no X08 images have started.
- Blind A v6 answered 11/13 Yes, with `payoffs` and `no_recap` No because the new merchandise-retention question lacks a direct callback and 124 stores is repeated without a marker. Blind B remains independent and pending; the two-reader combined gate is undecided. Keep video SHA fixed until both receipts arrive. Draft PR may present these as pending issues, not as a PASS.
- X05 is completing eight targeted semantic retakes and then incremental audio QA; its next planned load is 66 MiniMax images. X06 is preparing media separately. Shared judge quota previously around 924; all three 3-take worst cases (66 + 78 + 113 shots) could consume 771 judgments. Recheck remaining quota and full-batch feasibility before X08 image generation. This ticket is audio-only.
- Historical v7 independent source audit passed; v8 visual source audit failed an exit-fee timing implication; v9 chapter-title-only source delta passed. v9 blind A failed payoff and detour, blind B passed spoken required items, and both identified visual reveal-order problems. Their receipts remain version-bound and are not v10 approvals.
- v10 candidate main `video.json` SHA-256 `51185ca049c60cac3f009457a833b449f66bfafeb10fae8a5dee6076a94ea619`; Shorts remains `440ceee9649b30af2bd64ff1205bf38bff47d0be381b1b544cccff4601e2d543`. Third-chapter REDcard detour is replaced with source-backed 124-store/14.2m-sqft opening and FY2012–FY2014 margin/SG&A/depreciation/interest evidence. `x080312` now asks whether next-year merchandise margin catches SG&A; `x080438` answers US$714m→US$548m gap. Cards/prompts fix v9 early reveals. Lint 0/0 and docs-video tests pass; new independent v10 source and two blind receipts, incremental TTS and actual eight-minute body measurement are **pending**. No paid media while these gates remain open.
