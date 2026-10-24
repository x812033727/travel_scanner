---
id: 2026-10-24-c08-short-v8-safe-promotion
title: Promote C08 short v8 as guarded same-episode project
status: done
priority: P2
area: tools
owner: codex-c08-short-backend
claimed_at: 2026-10-24T05:13:46Z
created_at: 2026-10-24T05:13:41Z
completed_at: 2026-10-24T05:44:10Z
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

- [x] `--slug story-everyday-kikkoman-c08-short-v8` resolves the exact 36-line approved projection; the original 84-line C08 files remain byte-identical.
- [x] The reviewed 20-row plan points episode 8 to the short slug, retains its row identity, and leaves the other 19 rows unchanged.
- [x] Only the exact C08 project accepts a measured four-to-five-minute route; current timelines and checked frames remain mandatory.
- [x] The worker cannot overwrite approved C08 words or visuals with chapter generation or length resizing.

## Steps

- [x] Project frozen short-v8 files to a top-level slug directory and record source/projection hashes.
- [x] Re-certify C08 plan with an independent review, then rebuild `stories.json`.
- [x] Pin the initial C08 pronunciation snapshot before backend start, because the pre-authored `video.json` is not eligible for empty-story genesis.
- [x] Add exact C08 duration and worker guards, with focused tests.

## How to verify

Run `node tools/video/cli.mjs lint --slug story-everyday-kikkoman-c08-short-v8`, focused Node tests, `node docs/videos/brand-stories-everyday-reversals-20261020/build.mjs`, `node tools/video/long-form/cli.mjs check`, `npm run check:tasks`, and `git diff --check`. C15 PR #1810 was merged before the C08 lint change. Do not import, pay for media, upload, publish, or unpause the series here.

## Notes

The existing C08 task `2026-10-24-prepare-c08-kikkoman-canonical-video-project` on this branch owns the nested source package. This ticket owns only the paths listed in its scope. The owner approved a C08-only four-to-five-minute rewrite and exact v8 text/visual direction after seeing the 273.97-second paper body / 299.97-second paper total; neither is a measured duration. Current 84-line approvals do not transfer to the new slug. The 20-row series remains paused pending separate import, cost and release gates.

The independent C08 plan reviewer certified the revised source hash `5ccbe2040d8f93e975d5fa25922eee28662ab52f1e9cf007a8dd0f4e44acc839`; the rebuilt batch still has exactly 20 rows, with only C08's story/certification changed. An independent text-only pronunciation reviewer confirmed 36/36 frozen narration texts and the `MoMA` expansion; actual TTS listening stays HOLD. The pinned lexicon is a local immutable genesis of the current shared dictionary plus C08 plan names. `node --test --test-name-pattern='C08 short-v8 adopts' tools/video/automation/story.test.mjs` passed in a temporary ASCII `subst` drive (Windows Node test runner crashes on this Unicode worktree path). The worker adoption test reaches the mocked backend start only with the exact plan, keeps frozen docs, and records the outline gate in a temporary workdir.

C08 has no inherited US$25 paid cap: the historical C08 preflight explicitly says another episode's cap does not transfer. The worker requires a separate C08 owner-approved whole-film quote and cap receipt before paid stages, with quote no higher than that cap. The local test's US$25 and US$26 values are synthetic boundary examples, not an authorization or a proposed budget.

The 240-second QA exception is additionally bound to SHA-256 `31041c60a61f7612878e07417aaf7b7b914a70e04ad49ab395de6e8918c6d7d9` over all 36 ordered `[line.id,line.text]` pairs, and `1f3d6939b2d5dcf8983bda60ffd5a48b9a753ca2a9f5e0f6ed55453e4ef7079c` over ordered `[line.id,line.say,line.say_for]` pairs. A one-character visible narration edit or spoken override edit returns to the ordinary 480-second floor in the focused test, while a visual prompt edit leaves the narration predicate intact. This complements the worker's full-project hash guard.

Independent DURATION_ONLY source review and the four-file receipt were completed at `d9adb5b4b`; guarded CLI and receipt tests passed. The paper post-`say` total remains about 301.63 seconds, not measured media. Actual TTS and human listening, a measured body/final-cut pass, the `v7e03` diagram, picture QA, a C08 whole-film supplier quote and owner cap, production dry-run/import, upload and publication remain separate HOLD gates.

After that review, an independent QA CLI reproduction found that `needsMinimumLength(doc)` still passed `minMinutes: 8` to `assembleItem` for this explainer: a synthetic 9000-frame C08 cut passed the C08-only duration function but failed final QA as 05:00 under eight minutes. The follow-up `2026-10-24-close-exact-c08-short-v8-qa` narrows the CLI argument to the frozen approved C08 predicate and adds real CLI one-frame regression. The earlier DURATION_ONLY receipt is historical until a non-author reviewer rebinds it to the new source head. No synthetic fixture is a measured production cut or an owner listening approval.
