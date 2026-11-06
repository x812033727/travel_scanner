---
id: 2026-11-06-keyframe-judge-refuses-some-child-character
title: Keyframe judge refuses some child-character stills (PROHIBITED_CONTENT) since cute explainers get the cast identity check
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-06T17:41:19Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/keyframes.mjs
---

# Keyframe judge refuses some child-character stills (PROHIBITED_CONTENT) since cute explainers get the cast identity check

## Why

After PR #2028 cute explainers send the cast's reference sheets to the judge for an identity check. On
2026-11-06 the judge started answering 「AI 拒絕回應（PROHIBITED_CONTENT）」 for some stills of 原來如此事務所's
8-year-old girl: P07 `kid-hotter` on every take whatever the prompt (a plain cartoon face; three rewrites),
and P14 once mid-run. A refusal ends `keyframes` with exit 4, so one shot stops the whole episode.

## Definition of done

- [ ] A refused judge answer marks that one shot for review and the run goes on to the next shot.
- [ ] Find out whether the identity check (sheet + still of a child) is what triggers it; if so, word the
      request or the rubric so it is not refused.

## Notes

- Workaround used: `keyframes --shot <every other id>` to finish an episode, then pin the shot by hand.
