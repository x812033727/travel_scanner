---
id: 2026-09-30-video-worker-and-review-push-report
title: Video worker and review-push report the video's category
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-09-30T10:00:16Z
completed_at:
branch:
depends_on:
  - 2026-09-30-video-review-categories-column-browse-endpoint
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - .agents/skills/youtube-video/references/automated.md
---

# Video worker and review-push report the video's category

## Why

`video_projects.category` (migration 0116) is filled from the first report that carries it, but the
two places that report a tutorial to the site do not send it yet: the worker's `report()` in
`tools/video/automation/flow.mjs` and `review-push` in `tools/video/review/sync.mjs`. Both files
were held by other active tickets when the category landed, so worker-made tutorials are filed by
the owner on the page until this is done.

## Definition of done

- [ ] `flow.mjs` `report()` sends `category` when the state or video.json has one
      (`state.category ?? video.category`); the story pipeline's `category: "story"` reaches the site
      on the very first report.
- [ ] `review-push` sends `project.doc.category` when video.json has one.
- [ ] `.agents/skills/youtube-video/references/automated.md` §video.json 的重點 documents `category`
      (the eight codes, that the site fills only an unfiled video, that the owner can change it).

## Steps

- [ ] flow.mjs: read video.json once (there is already `recordedVideoId`) and spread
      `...(category ? { category } : {})` into the report body; automation.test.mjs asserts it.
- [ ] sync.mjs reviewPush body (next to `source_guide`); sync.test.mjs `--report-only` case asserts it.
- [ ] story.test.mjs: the first report body has `category: "story"`.
- [ ] automated.md bullet.

## How to verify

```bash
npm run test:tools
```
On the host after a worker round: `SELECT slug, category FROM video_projects WHERE last_synced_at > now() - interval '1 day'`.

## Notes

- The server never overwrites a category with a report (`admin_service.upsert_project`): sending it
  at every stage is safe. Do not change that rule.
- `VIDEO_CATEGORIES` lives in `tools/video/core/schema.mjs`; `validateVideo` already accepts the key.
