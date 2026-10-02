---
id: 2026-09-30-video-worker-and-review-push-report
title: Video worker and review-push report the video's category
status: done
priority: P2
area: tools
owner: claude-opus-5-5-report-category
claimed_at: 2026-10-01T23:53:03Z
created_at: 2026-09-30T10:00:16Z
completed_at: 2026-10-01T23:59:01Z
branch: claude/video-report-category
depends_on:
  - 2026-09-30-video-review-categories-column-browse-endpoint
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - .agents/skills/youtube-video/references/automated.md
  - tools/video/automation/story.test.mjs
---

# Video worker and review-push report the video's category

## Why

`video_projects.category` (migration 0116) is filled from the first report that carries it, but the
two places that report a tutorial to the site do not send it yet: the worker's `report()` in
`tools/video/automation/flow.mjs` and `review-push` in `tools/video/review/sync.mjs`. Both files
were held by other active tickets when the category landed, so worker-made tutorials are filed by
the owner on the page until this is done.

## Definition of done

- [x] `flow.mjs` `report()` sends `category` when the state or video.json has one
      (`state.category ?? video.category`); the story pipeline's `category: "story"` reaches the site
      on the very first report.
- [x] `review-push` sends `project.doc.category` when video.json has one.
- [x] `.agents/skills/youtube-video/references/automated.md` §video.json 的重點 documents `category`
      (the eight codes, that the site fills only an unfiled video, that the owner can change it).

## Steps

- [x] flow.mjs: read video.json once (there is already `recordedVideoId`) and spread
      `...(category ? { category } : {})` into the report body; automation.test.mjs asserts it.
- [x] sync.mjs reviewPush body (next to `source_guide`); sync.test.mjs `--report-only` case asserts it.
- [x] story.test.mjs: the first report body has `category: "story"`.
- [x] automated.md bullet.

## How to verify

```bash
npm run test:tools
```
On the host after a worker round: `SELECT slug, category FROM video_projects WHERE last_synced_at > now() - interval '1 day'`.

## Notes

- The server never overwrites a category with a report (`admin_service.upsert_project`): sending it
  at every stage is safe. Do not change that rule.
- `VIDEO_CATEGORIES` lives in `tools/video/core/schema.mjs`; `validateVideo` already accepts the key.
- Drama drafts and series episodes (`format: "drama"`, not stories) should report `category: "drama"`;
  the long-form drama pipeline, once it exists, reports `long-drama`.
- 2026-10-02 (claude-opus-5-5-report-category): claimed with --force over three stale claims
  whose PRs are merged: 2026-09-28-drama-listener-stale-check (codex-ten-drama, PR #978),
  2026-09-28-sothatswhy-shorts-from-episode (PRs #904/#950/#962) and
  2026-09-30-video-worker-moves-two-videos-at (PR #999).
- Scope: added `tools/video/automation/story.test.mjs`, because Steps asks it to assert that the
  first report of a brand story carries `category: "story"`.
- flow.mjs: `recordedVideoId()` became `recorded()`, which reads video.json once and returns the
  YouTube id and the category (`state.category ?? video.category`, kept only when it is one of
  `VIDEO_CATEGORIES`, so a stray value cannot make the site refuse the whole report). sync.mjs sends
  `project.doc.category` next to `source_guide` under the same check (loadProject does not lint).
- Drama drafts and series episodes are not reported as `drama` yet. The worker has no reliable
  way to tell them apart from other `format: "drama"` videos: a one-off with the flat-explainer
  preset is an explainer, and a series episode may belong to the 100-episode long-form line
  (`long-drama`). Guessing would file videos wrongly, and the server never overwrites a category
  once set, so a wrong guess would stick. Left for whoever adds an explicit kind for those
  pipelines; until then the owner files them on the page.
- automated.md lists ten codes, not eight: `drama` and `long-drama` were added to
  `VIDEO_CATEGORIES` after this ticket was written.
- Verified: the three new assertions (automation.test.mjs, story.test.mjs, sync.test.mjs) fail
  with the original flow.mjs and sync.mjs and pass with the change.
