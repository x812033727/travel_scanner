---
id: 2026-10-24-c08-short-v8-safe-promotion
title: Promote C08 short v8 as guarded same-episode project
status: in-progress
priority: P2
area: tools
owner: codex-c08-short-backend
claimed_at: 2026-10-24T05:13:46Z
created_at: 2026-10-24T05:13:41Z
completed_at:
branch: codex/c08-kikkoman-canonical-preflight-20261024
depends_on: []
scope:
  - docs/videos/story-everyday-kikkoman-c08-short-v8
  - docs/videos/brand-stories-everyday-reversals-20261020/episodes/C08.json
  - docs/videos/brand-stories-everyday-reversals-20261020/episodes/reviews/C08.json
  - docs/videos/brand-stories-everyday-reversals-20261020/stories.json
  - docs/videos/brand-stories-everyday-reversals-20261020/build.mjs
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
  - tools/video/core/duration.mjs
  - tools/video/core/duration.test.mjs
---

# Promote C08 short v8 as guarded same-episode project

## Why

The owner approved the exact C08 short-v8 narration and visual direction in this task. The reviewed projection is nested under the historical C08 folder, while the worker and CLI resolve `--slug` only to a top-level folder. The 20-row everyday series still points at the historical C08 slug. Promote the new slug without changing the original 84-line project or the other 19 episode rows.

## Definition of done

- [ ] `--slug story-everyday-kikkoman-c08-short-v8` resolves the exact 36-line approved projection; the original 84-line C08 files remain byte-identical.
- [ ] The reviewed 20-row plan points episode 8 to the short slug, retains its row identity, and leaves the other 19 rows unchanged.
- [ ] Only the exact C08 project accepts a measured four-to-five-minute route; current timelines and checked frames remain mandatory.
- [ ] The worker cannot overwrite approved C08 words or visuals with chapter generation or length resizing.

## Steps

- [ ] Project frozen short-v8 files to a top-level slug directory and record source/projection hashes.
- [ ] Re-certify C08 plan with an independent review, then rebuild `stories.json`.
- [ ] Add exact C08 duration and worker guards, with focused tests.

## How to verify

Run `node tools/video/cli.mjs lint --slug story-everyday-kikkoman-c08-short-v8`, focused Node tests, `node docs/videos/brand-stories-everyday-reversals-20261020/build.mjs`, `npm run check:tasks`, and `git diff --check`. The lint policy change in `tools/video/core/lint.mjs` waits for C15 PR #1810 merge. Do not import, pay for media, upload, publish, or unpause the series here.

## Notes

The existing C08 task `2026-10-24-prepare-c08-kikkoman-canonical-video-project` on this branch owns the nested source package. This ticket owns only the paths listed in its scope. The owner approved a C08-only four-to-five-minute rewrite and exact v8 text/visual direction after seeing the 273.97-second paper body / 299.97-second paper total; neither is a measured duration. Current 84-line approvals do not transfer to the new slug. The 20-row series remains paused pending separate import, cost and release gates.
