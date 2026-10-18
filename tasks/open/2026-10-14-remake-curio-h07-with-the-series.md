---
id: 2026-10-14-remake-curio-h07-with-the-series
title: Remake Curio H07 with the series look
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-curio-h07-v2
claimed_at: 2026-10-14T16:10:46Z
created_at: 2026-10-14T16:10:29Z
completed_at:
branch: codex/curio-h07-production-20261014
depends_on: []
scope:
  - docs/videos/curio-h07-v2
---

# Remake Curio H07 with the series look

## Why

The owner asked to fetch main, update the H07 branch and remake the episode under the new Curio series rules. The already approved `curio-h07` final was made with a custom adult editorial look and 59 illustrations among 99 body scenes. The new `curio-episode` lint requires the unchanged `cute-mystery` preset, at least 70% illustrated body scenes and no more than three cards in a row. Keep the approved original project and its media intact; produce the revision under the separate `curio-h07-v2` slug.

## Definition of done

- [x] The isolated H07 revision follows the fixed series look and passes `lint` with zero errors, including the illustration ratio and card-run checks.
- [ ] Its narration, illustrations, storyboard, final cut and selected en/ja/ko tracks have current source-bound evidence and pass their applicable review gates.
- [ ] The revised package and exact backend receipts are delivered for owner playback and private Studio upload; no publication is inferred from local QA.

## Steps

- [x] Fetch origin, rebase the H07 branch onto current main, guard PR #1497 against auto merge and audit the changed rules and active media state.
- [ ] Design all replacement shots and cards, verify historical claims, estimate the one-batch image count and spending cap, and record the owner budget decision before paid generation. The design, source check and quote are complete; owner cost decision is pending.
- [ ] Create the new slug and isolated workdir, verify reusable paid clip hashes, and bring the new project through lint, narration and full-storyboard review. The source, workdir, lint and cache audit are complete; four changed lines and all new images still need production and review.
- [ ] Render and inspect the final cut, finish en/ja/ko audio checks and captions against its actual timeline, package and submit the required backend reviews.

## How to verify

Run `node tools/video/cli.mjs lint --slug curio-h07-v2`, `check-audio`, `keyframes --dry-run`, `qa`, `package` and `review-push`/`review-pull` for the relevant gates. Inspect keyframe/contact-sheet receipts, exact audio/video frames, hashes, and the live `/admin/videos` review state. Run `npm run test:docs-videos` and `npm run check:tasks` before pushing. Keep YouTube Studio upload and publication as separate owner actions.

## Notes

- The original `curio-h07` backend project has an approved zh-TW final but no YouTube ID, upload readiness or publication. It must not be overwritten; the new rules require a fresh slug for an approved film's rewrite.
- Original H07 lint on main: six errors (custom style and negative, 59/99 shots, card runs of 5/5/4). The separate v2 now has 74/99 illustrated body scenes, a maximum three-card run and `lint` 0 errors/0 warnings. Source SHA-256: `80772F6204204F42F8A0B4905766EAE1A72635C6BDA73BFEA36F618D3A02771A`. Independent narrative review passed 11/11 and the source-bound historical/storyboard check passed.
- Old paid WAVs were copied into the isolated v2 workdir with source-key and hash checks. The final cache audit found 96/100 usable line clips in each of zh/en/ja/ko; IDs `45164df0`, `baeadea2`, `029cafbf`, `926246b2` must be resynthesized and all timelines rebuilt. Old audio QA and approvals do not transfer.
- All 59 old illustrations were compared with the series look; 0 are safe to reuse. The current 74-shot quote from `keyframes --dry-run --takes 3` is about US$1 for one full take, at most about US$3 for three takes; a US$4 all-in generation cap was submitted for owner decision. No paid v2 images have been generated.
- The new outline and script were submitted to `/admin/videos`. A live `review-pull` on 2026-10-15 still reports both `waiting for the owner`; do not start new narration or paid image generation until their current approvals and the cost cap are confirmed.
- Precommit verification on 2026-10-15: v2 `lint` 0 errors/0 warnings, independent data/code audit found no blocking issue, `git diff --check` clean, and the complete `test:docs-videos` suite passed 215/215 with bundled Node v24.19.0. System Node v24.13.0 reproducibly crashes the unrelated imported-long-languages child process with Windows exit `3221226505`.
- `npm run check:tasks` is blocked by an unrelated untracked duplicate of the already done H07 task under `tasks/open/2026-10-13-produce-curio-h07-man-in-the.md`. A prior policy block prevented removing that exact file; it is left untouched and not staged in this PR.
- PR #1497 remains draft and now has `no-auto-merge`; the rebased branch was force-pushed with lease after fetching origin. Do not merge until owner-controlled review is complete.
