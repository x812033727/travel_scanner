---
id: 2026-10-01-longform-duration-merge-integration
title: Integrate parallel long-video duration rules before merge
status: in-progress
priority: P1
area: tools
owner: codex-longform-integration
claimed_at: 2026-10-01T21:04:21Z
created_at: 2026-10-01T16:42:16Z
completed_at:
branch: codex/sothatswhy-season2-complete
depends_on: []
scope:
  - .agents/skills/youtube-video/SKILL.md
  - .agents/skills/youtube-video/references/automated.md
  - .agents/skills/youtube-video/references/formats.md
  - .claude/skills/youtube-video/SKILL.md
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/series.py
  - apps/api/migrations/versions/0117_video_min_8_minutes.py
  - apps/api/migrations/versions/0118_video_min_8_minutes.py
  - apps/api/tests/test_migration_0117_video_min_8_minutes.py
  - apps/api/tests/test_migration_0118_video_min_8_minutes.py
  - apps/api/tests/test_video_automation_settings.py
  - apps/api/tests/test_video_drama_requests.py
  - apps/api/tests/test_video_explainer_duration.py
  - apps/api/tests/test_video_series.py
  - apps/web/components/admin-video-explainer-duration.test.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-settings-tutorial.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - docs/videos/DESIGN.md
  - docs/videos/KNOWLEDGE-STORIES.md
  - docs/videos/README.md
  - docs/videos/long-form
  - docs/videos/so-thats-why/README.md
  - docs/videos/so-thats-why/season2/README.md
  - tasks/done/2026-10-01-video-min-8-minutes.md
  - tools/video/assemble/smoke.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/cli.test.mjs
  - tools/video/core/drama.mjs
  - tools/video/core/duration.mjs
  - tools/video/core/duration.test.mjs
  - tools/video/core/explainer.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/narration-locale.test.mjs
  - tools/video/core/schema.mjs
  - tools/video/core/stages.test.mjs
  - tools/video/core/state.test.mjs
  - tools/video/dubs/captions-package.test.mjs
  - tools/video/dubs/dubs.test.mjs
  - tools/video/dubs/freshness.test.mjs
  - tools/video/dubs/plan.test.mjs
  - tools/video/long-form
  - tools/video/media/clips.test.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/qa/checks.mjs
  - tools/video/qa/checks.test.mjs
  - tools/video/qa/cli.mjs
  - tools/video/qa/duration.test.mjs
  - tools/video/qa/qa.test.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/screencast/screencast.test.mjs
  - tools/video/templates/terminal/terminal.test.mjs
  - tools/video/tts/batch-recovery.test.mjs
  - tools/video/tts/check.test.mjs
  - tools/video/tts/tts.test.mjs
---

# Integrate parallel long-video duration rules before merge

## Why

Draft PR #1098 delivers the owner's five-catalog duration revision and actual-body QA floor. After its initial collision audit, a separate `claude/video-min-8-minutes` branch was submitted with general long-video duration rules. Neither duration implementation is on main at this audit. Their shared API/UI/QA paths must be integrated before merge so a later merge cannot reset the ten-minute catalog default or weaken the measured body minimum.

## Definition of done

- [ ] Inspect the latest main and both duration heads; reuse any implementation already landed and resolve only the remaining duration overlap.
- [ ] All 473 effective plans retain their reviewed targets, covered/rejected statuses and original source hashes; requests keep a ten-minute explainer default and accept every reviewed catalog target.
- [ ] QA retains the actual body and final cut minimum of 14,400 frames at 30 fps, with current speech/frame bindings and bookends excluded from the body.
- [ ] Review affected SHA changes independently, refresh the genuine review receipt, and pass required CI for the final combined head before merge.

## Steps

- [ ] Compare `origin/claude/video-min-8-minutes` and PR #1098 with latest main; check whether the peer branch now has a PR.
- [ ] Resolve shared schemas.py, series.py, admin-video-series.tsx, KNOWLEDGE-STORIES.md, so-thats-why/README.md and QA checks/CLI hunks on the eventual integration branch, without modifying another owner's branch or completed ticket.
- [ ] If adopting the peer migration, coordinate its 0117 revision collision with #1097 and extend the migration task scope before edits; never leave two unplanned Alembic heads.
- [ ] Run both implementations' regression cases and all catalog/review checks; retain the draft/no-auto-merge gate until the combined revision is reviewed and CI is green.

## How to verify

Run `node tools/video/long-form/cli.mjs check`, the four new long-form/core/QA Node test files, `npm run test:tools`, the API explainer/drama/series/story suites, the two admin explainer/series UI suites, web typecheck/i18n, and `npm run check:tasks`. Check all four required CI jobs on the final combined SHA.

## Notes

Continuation claim audit on 2026-10-02: the six refusing claims are September 27/28 review or stale records with no current worktree or remote for their former branches. Their document/Shorts implementations already landed (#978/#904). This claim is forced only for duration integration hunks; no other owner's task is closed/released or hand-edited. The completed peer task is imported byte-identically as Git provenance. Submitted #1094/#1097/#1100 still share files but change distinct production/Shorts/thumbnail paths; integration retains their latest main changes and all subsequent merges require current CI.

The expanded scope lists the 55 peer-submitted files and this revision's existing plan/review paths explicitly. Only the duration work will be integrated onto this draft; another owner's branch is not changed. Migration numbering will follow the actual landed head at final rebase, with a single-head check before push.

2026-10-02 audit: main is `abbc276d409e9ac5e1e5c765792b569b14f99588`; the peer branch advanced from `ae773c20` to `5851bd8b` after this revision's initial audit. No peer PR appeared in the latest open-PR listing. The peer branch chooses flat-explainer 8–12/default 8 and a general final-cut floor; PR #1098 chooses 8–20/default 10 and a separate measured-body floor for the five requested catalogs. These differences require deliberate integration, not a blind conflict pick. Other submitted PRs #1085/#1097/#1100 touch shared files in unrelated character/Shorts/thumbnail hunks. Neither media generation, production activation nor merge is authorized by this integration ticket alone.

PR #1098: https://github.com/x812033727/travel_scanner/pull/1098 . Its planning/input/runtime implementation is locally complete and independently reviewed. This open ticket records the later shared-branch integration requirement; it does not imply the reviewed plans are measured or published videos.

Before final delivery, main advanced to `eda3b60f` and #1098 rebased onto it. #1085's character-look validation is now incorporated; its affected API suite passes 105 tests with three database skips. The peer duration branch still has no PR in the latest head-filtered listing.

Independent collision audit at peer `5851bd8b`: three unmerged commits change 55 files; seven files overlap this revision. The peer adds global worker/lint/settings/DB changes outside this revision's five-catalog rule. Its `0117_video_min_8_minutes` and #1097's `0117_video_shorts_topics` both point to `0116_video_project_category`; this PR itself adds no migration. The eventual integration must resolve that peer/Shorts migration collision before adopting both. #1094 also edits series.py; #1100 edits QA cli. Old batch #1083 has 17 intersecting season-2 source/validator/task paths already byte-preserved in this total PR; determine merge order and reuse landed bytes, without modifying that author's PR state.
