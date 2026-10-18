---
id: 2026-10-17-a01-public-sources-from-cited-claims
title: A01 public sources from cited claims only
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-17T23:43:02Z
completed_at:
branch:
depends_on:
  - 2026-10-17-a01-seven-to-eight-minute-measured
scope:
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
---

# A01 public sources from cited claims only

## Why

For A01 `story-rolling-suitcase-v2`, `composeStory` currently copies every
`plan.sources` entry into the public `video.json.sources`. The reviewed plan has
23 URLs, while the r11 six-chapter draft's effective scene claims cite 16 of
them. Unused plan research should not appear as a source for the finished
story, and future chapter remerges must not restore it. This is a source-index
and editorial-integrity fix separate from the seven-to-eight-minute runtime.

## Definition of done

- [ ] A01's public sources contain only source indexes cited by effective
      non-`NOT FOUND` claim rows in the current six chapters, preserving plan
      order and source metadata.
- [ ] B18 and other stories keep their current source behavior until their
      own reviewed evidence and requirements authorize a change.
- [ ] A fresh and repeated chapter remerge cannot restore uncited A01 URLs.

## Steps

- [ ] Confirm the r11 chapter source indexes against the frozen A01 plan and
      independent factual review; do not infer them from the old r8 video.json.
- [ ] Implement the A01-only filter in `composeStory`, covering partial and
      complete chapter merges without invalid indexes or false citations.
- [ ] Add tests for 23-to-16 A01 sources, `NOT FOUND` exclusion, stable order,
      remerge, and unchanged B18 output.

## How to verify

Run `node --test tools/video/automation/story.test.mjs`, `npm run check:tasks`
and the bound long-form duration check if any bound file changes. Compare the
resulting A01 `video.json.sources` with independently reviewed claim evidence.

## Notes

2026-10-18: Filed unclaimed at the owner's request while the duration task
still owns `story.mjs`/`story.test.mjs`. Start only after that task's changes
are integrated and its claim is released. Preserve #1518 and any production
chapter/media artifacts; no host rewrite or upload is authorized by this file.
