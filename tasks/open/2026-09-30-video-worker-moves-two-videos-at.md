---
id: 2026-09-30-video-worker-moves-two-videos-at
title: Video worker moves two videos at once
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-30T01:13:28Z
created_at: 2026-09-30T01:12:48Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/cli.mjs
  - tools/video/automation/automation.test.mjs
  - docker-compose.prod.yml
  - .agents/skills/youtube-video/references/automated.md
---

# Video worker moves two videos at once

## Why

The worker moved one video per unit, oldest first. On 2026-09-30 gemini-connected-apps and
meta-anti-scam sat still for twenty minutes and more behind google-vids' four caption languages
(five to ten minutes each), and the owner read that as 卡住. The owner asked for two at once.

## Definition of done

- [x] `auto` runs `VIDEO_WORKER_LANES` lanes (default 1, at most 3); production sets 2.
- [x] Two lanes never move the same video: a shared `busy` set of slugs, claimed before the
      first await of a unit and released when it ends.
- [x] Only the first lane drops, takes retries, records pasted addresses, answers discussions,
      starts series episodes, drama requests and drafts; a second lane only moves videos
      already under way, so nothing new is started twice.
- [x] The container's memory limit goes from 3g to 5g, since two lanes may each render.

## How to verify

`node --test tools/video/automation/automation.test.mjs` (the two-lanes and lane-count tests).
After the deploy, the worker log shows `[lane 2]` lines while the first lane moves another video.

## Notes

- Which lane takes the oldest video is a matter of timing; the test only asserts they differ.
- Setting `VIDEO_WORKER_LANES: "1"` in docker-compose.prod.yml goes back to one at a time.
