---
id: 2026-09-27-five-binge-story-plans
title: Five original 120-minute drama production plans
status: done
priority: P1
area: docs
owner: codex-five-binge
claimed_at: 2026-09-27T17:25:34Z
created_at: 2026-09-27T17:24:28Z
completed_at: 2026-09-27T18:14:04Z
branch: codex/five-binge-story-plans
depends_on: []
scope:
  - docs/videos/series-plans/binge-five-20260928
---

# Five original 120-minute drama production plans

## Why

The owner approved five original 120-minute drama plans and requested complete production documents. The existing pipeline needs full setting books, 40-episode outlines, four chapter documents, continuity ledgers and packaging copy, rather than only pitches in chat. This task prepares offline files and does not create production series or generate paid media.

## Definition of done

- [x] Five setting books, 200 detailed episodes across 20 chapters, continuity ledgers and three packaging variants per series are complete.
- [x] All plans pass the existing worker document validator and cross-chapter continuity checks.
- [x] Independent editorial reviews are bound to the final source hashes and no blocking findings remain.
- [x] Delivery clearly distinguishes planned timing/casting from measured audio/video and actual publication.

## Steps

- [x] Inspect current pipeline, verify task/worktree/remote/PR collision scope, claim isolated document path.
- [x] Define a shared authoring contract, deterministic document builder and read-only validator.
- [x] Complete five authored source packs and independent review/fixes.
- [x] Build all readable/structured files, run checks, write the handoff and close this task.

## How to verify

- `node docs/videos/series-plans/binge-five-20260928/build.mjs`
- `node docs/videos/series-plans/binge-five-20260928/validate.mjs --require-reviews --write-report`
- `node --test docs/videos/series-plans/binge-five-20260928/validate.test.mjs`
- `npm run check:tasks`

## Notes

- Worktree was detached at 853a3434; created codex/five-binge-story-plans. Existing untracked .codex/environments/ is not part of this task.
- Repository task timestamps use UTC (2026-09-27); the owner-approved batch date is 2026-09-28 Asia/Taipei.
- Scope had no active task or open PR collision. Other video branches target different work.
- youtube-video calls for an independent verifier. Authors work only in allocated source.mjs paths; reviewers assess other authors' work.
- First four series explicitly use no-romance; the fifth uses custom + dual-male-leads-subtext so it receives the same retention checks.
- Closed finale uses a resolved emotional reversal, compatible with the current chapter-ending type checks without inventing a sequel cliffhanger.
- No production host commands, admin requests, media API calls, uploads, pushes or deployment are part of this document batch.
- All five sources contain 40 authored episodes, four chapters, ten resolved mystery threads and three packaging variants. Each series builds 20 readable/structured files, with source and editorial receipts kept separately.
- The 14 local validator tests passed, including cross-chapter endings, early/missing payoffs, missing cast/location references, stale reviews, non-independent reviewers and unresolved findings.
- Existing repository-wide task warnings concern older claims and unrelated overlapping scopes; the task check exited successfully. These are not newly introduced by this batch.
- Final `validate.mjs --require-reviews --write-report` passed for all five series: 200 episodes, 30 production documents, matching generated files and independent review hashes, no errors.
- Final package has 118 text files. All 72 relative Markdown links resolve; JSON parses, encoding, whitespace and conflict-marker checks passed.
- Entry point: docs/videos/series-plans/binge-five-20260928/README.md. REVIEW.md records the actual editorial corrections; PRODUCTION.md defines the later first-three-episode calibration and measured media acceptance.
- Delivered locally without Git commit/push/PR. No full dialogue scripts, images, voice/audio, captions, videos, backend creation or publishing were performed.
