---
id: 2026-10-02-anime-long-episode-support
title: Support long anime episodes and closed finales
status: done
priority: P2
area: tools
owner: codex-root
claimed_at: 2026-10-02T16:14:44Z
created_at: 2026-10-02T04:47:57Z
completed_at: 2026-10-02T16:17:12Z
branch: codex/anime-long-production
depends_on: []
scope:
  - apps/api/app/video_automation/anime_policy.py
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/series.py
  - apps/api/app/video_automation/judge.py
  - apps/api/app/video_automation/settings.py
  - apps/api/migrations/versions/0122_video_anime_production_policy.py
  - apps/api/tests/test_video_anime_production_policy.py
  - apps/api/tests/test_migration_0122_video_anime_production_policy.py
  - apps/api/tests/test_migration_0121_video_series_planning.py
  - apps/api/app/video_reviews/schemas.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_anime_review_policy.py
  - apps/api/tests/test_video_review_renewal.py
  - apps/api/tests/test_video_shorts.py
  - tools/video/automation/series.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/automation/discuss.mjs
  - tools/video/automation/discuss.test.mjs
  - tools/video/automation/anime-write.mjs
  - tools/video/automation/anime-write.test.mjs
  - tools/video/core/anime-policy.mjs
  - tools/video/core/anime-policy.test.mjs
  - tools/video/core/branding.mjs
  - tools/video/core/branding.test.mjs
  - tools/video/core/schema.mjs
  - tools/video/core/screenplay.mjs
  - tools/video/core/screenplay.test.mjs
  - tools/video/core/state.mjs
  - tools/video/core/state.test.mjs
  - tools/video/core/approvals.mjs
  - tools/video/core/approvals.test.mjs
  - tools/video/core/drama.mjs
  - tools/video/core/drama.test.mjs
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/duration.mjs
  - tools/video/core/duration.test.mjs
  - tools/video/core/timeline.mjs
  - tools/video/core/timeline.test.mjs
  - tools/video/tts/cli.mjs
  - tools/video/tts/synthesis.mjs
  - tools/video/tts/tts.test.mjs
  - tools/video/assemble/cli.mjs
  - tools/video/assemble/assemble.test.mjs
  - tools/video/qa/checks.mjs
  - tools/video/qa/cli.mjs
  - tools/video/qa/duration.test.mjs
  - tools/video/package/cli.mjs
  - tools/video/package/package.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/production/anime-input.mjs
  - tools/video/production/anime-input.test.mjs
  - apps/web/components/admin-video-series.tsx
  - apps/web/components/admin-video-series.test.tsx
  - apps/web/components/admin-video-review-card.tsx
  - apps/web/components/admin-video-reviews.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - docs/videos/LONG-ANIME-PRODUCTION.md
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
  - tools/video/long-form/review.mjs
---

# Support long anime episodes and closed finales

## Why

The Borrowed Dawn anime plan preserves the owner's 22-minute story / 30-minute broadcast-slot specification and a quiet closed finale. Current ordinary drama SeriesIn inputs reject more than 8 minutes; the custom genre forces two satisfaction beats per episode; chapter validation forces the final tension score to remain at least 4. Filing a video as anime in PR #1110 changes none of those rules. Do not shorten the story, change it to a nonfiction story/explainer, or fabricate satisfaction beats to bypass them.

## Definition of done

- [x] An explicit long-anime production policy accepts the intended body duration without relaxing existing shorts, knowledge-video or ordinary-drama guards.
- [x] Ensemble tragedy and a closed final episode can retain their actual beat and ending policies while ordinary serial episodes keep meaningful checks.
- [x] The API, writer budgets, narration timeline, media QA and admin UI agree on body, OP/ED and broadcast-slot duration.
- [x] The plan can be converted into a documented, validated input without claiming that its current planning JSON is an executable SeriesIn request.

## Steps

- [x] Read docs/videos/series-plans/borrowed-dawn/plan.json and the independent content review before designing the policy.
- [x] Trace all duration and retention consumers and narrow the implementation scopes before claiming this task.
- [x] Add meaningful acceptance and boundary regressions; verify the final-episode exception is restricted to the declared last episode of a closed series.
- [x] Document body versus OP/ED/slot budgets and prepare a validated draft input; leave media generation, activation and publication to their separately authorized workflows.

## How to verify

Run the affected API schema/series tests and Node duration/series/QA tests, web checks if the editor is changed, and npm run check:tasks. Demonstrate a 22-minute anime input succeeds, an invalid duration fails, ordinary drama's 8-minute boundary remains intact, an early episode cannot use the closed-final exception, and the supplied plan still has 120 episodes and a closed ending. No paid provider or production call is needed to validate these boundaries.

## Notes

Recorded while organizing a separate content PR at the owner's request. This is production support, not unfinished content collation. Existing evidence: apps/api/app/video_automation/schemas.py defines SERIES_MAX_MINUTES = 8 and SeriesIn; tools/video/automation/series.mjs requires tension[4] >= 4 and applies GENRE_SPECS.custom retention rules. PR #1110 supplies only the anime category and its migration.

The owner now asked to continue unfinished tickets. PR #1125 is merged. Before claiming, three independent read-only traces found that the original four-file scope omitted persistence, writer capacity, silent-action timing, verdicts and measured QA/package gates, so the narrow concrete paths above cover those necessary consumers. The original borrowed-dawn package is untouched because draft PR #1131 owns its story polish. PR #1129 changes branding and PR #1130 changes Shorts; neither owns these implementation paths. Two old API review claims still overlap schemas.py but are stale, have no local worktree/remote branch/open PR and are not modified or released here; force-claiming this existing ticket is limited to that stale overlap.

Frozen implementation contract: production_policy is the explicit string long-anime-v1 and runtime_spec stores body_target_seconds, op_ed_budget_seconds, broadcast_slot_seconds and slot_reserve_seconds. Their sum must match the slot. Target body supports whole minutes 9–30 only through this profile; the authored request remains 1320/180/1800/300 seconds and ensemble. Measured body tolerance is explicitly fixed at ±60 seconds (21–23 for the 22-minute target), with actual OP/ED within its budget and presentation within slot minus reserve. OP/ED is a budget, not mandatory generated footage or proof of 180 seconds of assets; existing channel branding limits remain. Reserve is never generated padding. New profile drafts start paused, original planning-only rows stay locked, and no paid provider or live production action is part of this coding work.

Independent review expanded the concrete consumer scope to cover scheduler status, byte-identical approval renewal, silent-action screenplay content, action position, natural-speed clip fitting and neighboring cached episode edits. Runtime approvals bind actual server episode identity and strict measured frame proof; changing a worker label cannot downgrade a native episode to ordinary rules. All native reviews remain manual despite global shortcuts. Changed budgets do not buy unchanged voice clips again. The offline adapter retains all 12 source documents, 120 episodes and 240 distinct tension events, and explicitly lists 16 missing cast voices with ready_for_production=false.

Concurrent PR #1132 later appeared with separate drama audio-evidence and localization retention work on overlapping pipeline paths and the shared duration receipt. This branch does not copy its unmerged implementation or change its task. Rebase and rerun the current-file duration receipt if either draft lands first. PR #1131 still owns story polish; the original borrowed-dawn source package remains untouched here. The final branch incorporates merged branding PR #1129 before installing its independent receipt.

Completed validation: 540 affected API/database tests passed with RUN_INTEGRATION_TESTS=1 on an isolated PostgreSQL 17; the final post-rebase native/create/review batch passed 131 tests without skips. Full Python Ruff and Mypy passed (815 files). Full web suite passed 3,795 tests; the final silent-action/coverage UI change passed 64 focused tests and the independent reviewer separately passed 97 current component tests. Web lint, all five locales/25 namespaces, typecheck and production build passed. Final npm run test:tools passed 1,336 tests, failed zero and retained one pre-existing optional smoke skip. The independent DURATION_ONLY increment binds 108 current files, preserves the 70 historical paths and checker logic, and passed all 473 plans plus the receipt regressions. npm run check:tasks and git diff --check passed. The concrete offline draft was regenerated and still has ready_for_production=false. The owned PostgreSQL test container was stopped and removed; no real provider, production host, activation or publication was used.

Full API CI follow-up: run 37028620116 found 71 failures caused by isolated SQLite fixtures missing video_drama_series/video_drama_episodes, while 6,420 tests passed. Reopened this own ticket and narrowly expanded scope to the two fixture owners above; test_video_long_review_renewal.py reuses the renewal fixture and needs no source edit. Preserve the real database episode-authority guard and fix the fixture schema, then run all three affected modules and independently verify ordinary/native behavior before reclosing.

Resolved CI follow-up: only the two existing SQLite fixtures changed their model imports/table lists; all test bodies and assertions, the shared long-review fixture alias and every production guard remain unchanged. All three affected suites now pass 126 tests with no skips, independently rerun by the separate reviewer (126 passed), plus scoped Ruff, Mypy and task/whitespace checks. The independent reviewer confirmed all 108 current duration bindings, all 473 plans and receipt tests 2/2 still pass; fixture-only paths require no receipt rebinding. Initial CI passed 6,420 other API tests; the same draft PR will rerun the complete required checks on these fixed bytes.
