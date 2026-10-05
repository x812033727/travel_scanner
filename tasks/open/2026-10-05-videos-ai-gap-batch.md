---
id: 2026-10-05-videos-ai-gap-batch
title: Admin queue for a slides video of a chosen article, and the eight AI-gap videos through it
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-05T08:42:41Z
created_at: 2026-10-05T02:52:28Z
completed_at:
branch: claude/determined-clarke-1laipc
depends_on: []
scope:
  - apps/api/app/video_automation/models.py
  - apps/api/app/video_automation/schemas.py
  - apps/api/app/video_automation/topics.py
  - apps/api/app/video_automation/slides_requests.py
  - apps/api/app/video_automation/admin_api.py
  - apps/api/migrations/versions/0126_video_slides_requests.py
  - apps/api/tests/test_migration_0126_video_slides_requests.py
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

# Eight videos from the AI income, investing, head-to-head and office batches

## Why

Describe the problem in the terms someone who has never seen it would need.

## Definition of done

- [ ] The observable outcome, not the implementation.

## Steps

- [ ] First sub-task.
- [ ] Second sub-task.

## How to verify

The exact commands or clicks that prove it works.

## Notes

Findings, decisions and dead ends, so the next agent does not repeat them.
