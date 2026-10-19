---
id: 2026-10-19-count-brand-stories-apart-from-the
title: Count brand stories apart from the worker's waiting-draft cap
status: done
priority: P2
area: tools
owner: claude-opus-5-5-story-room
claimed_at: 2026-10-19T00:46:29Z
created_at: 2026-10-19T00:34:35Z
completed_at: 2026-10-19T02:28:16Z
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/series.mjs
  - tools/video/automation/series.test.mjs
  - .agents/skills/youtube-video/references/series.md
---

# Count brand stories apart from the worker's waiting-draft cap

## Why

The worker starts a new video only while fewer automated videos are active than
`max_waiting_drafts` (`room()` in `tools/video/automation/flow.mjs`, at most 10). Brand
stories and the hourly news slides share that one count, so on 2026-10-18 ten news slides
held the fifth adapted story (B26, `brand-stories-adapt`) for hours although its own limit
(`drama.series_max_in_flight`) had room. The owner asked (2026-10-19) that brand stories be
counted on their own.

## Definition of done

- [x] A brand story (series `kind: "story"`) starts whenever the site's story quota allows it
      (series pause, per day, `series_max_in_flight`, per month, upload buffer), however many
      other drafts are waiting.
- [x] Active brand stories no longer take places from `max_waiting_drafts`: news, slides,
      one-off dramas and other series episodes count only each other.
- [x] The skill references say so.

## Steps

- [x] `room()` leaves brand stories out of the count; `seriesStep` skips it for a story episode.
- [x] Tests in `series.test.mjs`.
- [x] series.md (references are not mirrored under .claude/skills).

## How to verify

```bash
node --test tools/video/automation/story.test.mjs tools/video/automation/series.test.mjs tools/video/automation/automation.test.mjs
npm run test:tools
```

## Notes

- The server's own story quota (`story_quota` in `apps/api/app/video_automation/series.py`)
  already holds a story back when its limits are reached, so the worker needs no second cap.
- Claimed with `--force` on 2026-10-19 (owner's choice): `flow.mjs` and `series.test.mjs` also sit in the
  scopes of 2026-10-16-bind-story-audits-and-narration-to and 2026-10-14-ai-and-tech-videos-tell-one;
  this change touches only `room()` and one new test.
- Local run 2026-10-19: series, story and automation test files 368/368.
