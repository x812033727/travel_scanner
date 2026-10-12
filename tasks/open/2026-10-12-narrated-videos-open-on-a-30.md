---
id: 2026-10-12-narrated-videos-open-on-a-30
title: Narrated videos open on a 30-60 s curiosity condensation before the first real chapter
status: review
priority: P1
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-12T06:04:09Z
created_at: 2026-10-12T06:03:44Z
completed_at:
branch: claude/video-intro-30sec-summary-2366ac
depends_on: []
scope:
  - tools/video/core/lint.mjs
  - tools/video/core/lint.test.mjs
  - tools/video/core/cadence.mjs
  - tools/video/core/cadence.test.mjs
  - tools/video/automation
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
  - docs/videos/ILLUSTRATED.md
  - docs/videos/STORY.md
  - docs/videos/history-curiosity/README.md
---

# Narrated videos open on a 30-60 s curiosity condensation before the first real chapter

## Why

The owner (2026-10-12): before the real content starts, a narrated video needs 30 seconds or more
of condensed content whose job is to make the viewer curious enough to stay to the end. The rules
said the opposite: the opening chapter was to land within 30 s (20 s for illustrated slides and
the explainer series), and lint warned when it ran longer. The owner chose a narrated curiosity
condensation (not an edited montage of later clips) for teaching cards, illustrated storytelling
(the explainer series included) and brand stories; dramas with a cast and the manual route keep
their openings.

## Definition of done

- [x] lint warns when an episode's opening chapter is under 30 s or over 60 s (a drama with a
      cast keeps its 30 s hook; compilations and fixture-length examples are not read).
- [x] The table-of-contents warning covers the whole condensation (60 s).
- [x] Planner, writer and listener prompts of the slides route, the explainer route, the two
      profiled explainer series and the brand story describe the condensation; outlines carry a
      開場濃縮 line; a brand story's hook budget is 45 s.
- [x] script-writing.md §開場濃縮, formats.md, automated.md, ILLUSTRATED.md, STORY.md and the
      history-curiosity README say the same.

## How to verify

```bash
node --test tools/video/core/lint.test.mjs tools/video/core/cadence.test.mjs
node --test tools/video/automation/*.test.mjs
npm run test:tools
```

## Notes

- The explainer instruction digests (prompts.test.mjs, explainer-series.test.mjs,
  series.test.mjs) were re-pinned on purpose. Their comment holds: the instructions are part
  of a stage's inputs, so an explainer episode unfinished on the host when this deploys has
  that stage asked, and paid for, again. Deploy with none unfinished.
- Not done, for a later task if the owner wants it: the channel's intro bumper (BRANDING.md) still
  plays before the first line, so the condensation starts after it. Moving the bumper after the
  condensation (cold open → bumper → chapter 2) is an assemble change.
- An edited montage of real later clips as the condensation was the owner's other option; not
  chosen.
- docs/videos/so-thats-why/README.md §一集長什麼樣 still says 鉤子 0:00–0:20. It is in the
  scope of 2026-10-10-sothatswhy-minimax-images, active when this was written, so it was left
  alone; the prompt (explainer-series.mjs) is what the worker reads. Whoever holds that file
  next: make the row 開場濃縮 0:00–0:30 至 1:00, as history-curiosity/README.md has it.
