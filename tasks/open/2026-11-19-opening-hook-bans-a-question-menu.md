---
id: 2026-11-19-opening-hook-bans-a-question-menu
title: Opening hook bans a question menu (curio, story, sothatswhy)
status: in-progress
priority: P2
area: tools
owner: claude-opus-elegant-hypatia
claimed_at: 2026-11-19T00:58:25Z
created_at: 2026-11-19T00:57:58Z
completed_at:
branch: claude/elegant-hypatia-07i3yx
depends_on: []
scope:
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
  - tools/video/core/curio.mjs
  - docs/videos/so-thats-why/dialogue-pilot-20261103/README.md
  - docs/videos/lessons/sothatswhy.md
  - docs/videos/lessons/curio.md
  - .agents/skills/youtube-video/references/script-writing.md
---

# Opening hook bans a question menu (curio, story, sothatswhy)

## Why

Owner 2026-11-19: 「開場鉤子禁疊問題菜單」. Openings of 奇聞檔案局, the brand stories and
原來如此事務所 stack three or more questions back to back (「為什麼…？為什麼…？那…呢？」), which reads
like a menu of what the video will cover instead of one hook. 黑猫研究院 opens on ONE question or
situation, then its contrast and the promise. The owner also asked to put the rule into the
sothatswhy template (dialogue-pilot README) and to change the tools.

## Definition of done

- [x] lint warns (kind "narrative") when a curio-, story- or sothatswhy- script asks more than two
      questions in its opening (first chapter, at most 90 s; first 60 s without chapters).
- [x] The rule is written in the sothatswhy template, lessons (curio, sothatswhy) and script-writing.md.

## How to verify

```bash
node --test tools/video/core/narrative.test.mjs && npm run test:tools && npm run test:docs-videos
```

## Notes

- The check is called from `curio.mjs` `pacingWarnings`, not `lint.mjs`: lint.mjs is bound by the
  independent duration review (`tools/video/long-form/review.mjs` REVIEW_FILES), and lint already
  calls `pacingWarnings` for every video.

- The second half of the owner's request (「以後開頭就不要有片頭了，直接開始」) needs
  tools/video/core/branding.mjs and tools/video/assemble/branding.mjs, which two stale October
  claims still list (2026-10-12-lengthen-the-channel-outro-to-20, 2026-10-24-episodes-of-a-compilation-series-carry).
  Filed separately as 2026-11-19-heimao-series-start-with-no-intro, waiting for the owner to allow
  taking over those stale scopes.
