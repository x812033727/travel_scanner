---
id: 2026-10-05-videos-ai-gap-batch
title: Admin queue for a slides video of a chosen article, and the eight AI-gap videos through it
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-05T08:42:41Z
created_at: 2026-10-05T02:52:28Z
completed_at: 2026-10-06T13:35:08Z
branch: claude/determined-clarke-1laipc
depends_on: []
scope:
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/topics.py
  - apps/api/app/video_automation/slides_requests.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/migrations/versions/0127_video_slides_requests.py
  - apps/api/tests/test_migration_0127_video_slides_requests.py
  - apps/api/tests/test_video_slides_requests.py
  - apps/api/tests/test_video_automation_ai.py
  - apps/web/app/api/video/automation/slides-requests
  - apps/web/components/admin-video-slides-requests.tsx
  - apps/web/components/admin-video-slides-requests.test.tsx
  - apps/web/components/admin-video-reviews.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/automation/automation.test.mjs
  - docs/videos/AUTOMATION.md
---

# Admin queue for a slides video of a chosen article, and the eight AI-gap videos through it

## Why

The owner wants eight videos from the new AI income and investing articles, started from the
admin. The admin had no way to do that: the worker's planner chose its own topic from recent
articles and a web search, and the drama request queue turns every request into a one-off
drama series.

## Definition of done

- [x] `video_slides_requests` (migration 0127; renumbered from 0126 after #1345 took 0125) with admin routes (list, file, withdraw) and
      worker routes (next, start, done); a request is refused while automation is off, for an
      article that is not a published zh-TW life article, one already queued or started, or
      one a live slides video already retells.
- [x] The worker takes a request after drama requests and before the scheduled draft, plans
      only that article (variant-free, so it counts toward max_drafts_per_month), keeps it
      through a re-plan and reports done on publish approval.
- [x] The tutorials tab shows the queue and, for content managers, the form (five locales).
- [x] Long-form duration receipt rebound by an independent DURATION_ONLY review (10 files):
      a requested video keeps the eight-minute floor.
- [x] API, web, tools suites green; PR #1268 CI green.
- [ ] After deploy: the owner queues the eight videos (order and the finance note are in the
      PR description).

## Notes

- Implemented by a workflow: three layer implementers against one contract, four adversarial
  reviewers (8 confirmed findings: an idempotent start for a retried claim, a per-article
  advisory lock against double filing, only the two "withdrawn" 409s end a claim, i18n
  wording, a heading level, tests for the room() gate), then fixes.
- The e2e runtime API needed the new admin list (`{requests: []}`), or the admin video specs
  saw a 404; fixed in 2f93043b.
- A crash between the claim and the worker saving its state leaves an orphan `started`
  request that blocks re-queueing that article; the same window exists for drama requests.

- Closed by claude-opus-5-5-train-1323-1324-1268 in the train for #1323, #1324 and #1268
  (the claim was over 24 hours stale and the branch work is complete). The unticked production
  step moved to `2026-10-06-publish-the-eighteen-life-ai-articles`.
