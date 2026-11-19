---
id: 2026-11-19-heimao-titles-and-retitle-batch
title: Heimao-style titles for curio, story and sothatswhy; retitle batch for the old episodes
status: in-progress
priority: P1
area: tools
owner: claude-opus-elegant-hypatia
claimed_at: 2026-11-19T10:00:06Z
created_at: 2026-11-19T06:30:00Z
completed_at:
branch: claude/elegant-hypatia-07i3yx
depends_on: []
scope:
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
  - tools/video/automation/explainer-series.mjs
  - tools/video/automation/explainer-series.test.mjs
  - docs/videos/packaging-refresh-20261111/curio-20261119-a.md
  - docs/videos/packaging-refresh-20261111/curio-20261119-a.json
  - docs/videos/packaging-refresh-20261111/curio-20261119-b.md
  - docs/videos/packaging-refresh-20261111/curio-20261119-b.json
  - docs/videos/packaging-refresh-20261111/story-20261119.md
  - docs/videos/packaging-refresh-20261111/story-20261119.json
  - docs/videos/packaging-refresh-20261111/sothatswhy-20261119.md
  - docs/videos/packaging-refresh-20261111/sothatswhy-20261119.json
  - docs/videos/packaging-refresh-20261111/README.md
  - docs/videos/so-thats-why/dialogue-pilot-20261103/README.md
  - docs/videos/lessons/curio.md
  - docs/videos/lessons/sothatswhy.md
---

# Heimao-style titles for curio, story and sothatswhy; retitle batch for the old episodes

## Why

Owner 2026-11-19: 「標題是不是也要好好的研究一下」「先照黑貓的方式做，舊集標題也一起改」. 原來如此's
title rule was one line; the curio rule lived only in prompts; nothing checked titles.

## Definition of done

- [x] `narrative.mjs` `titleProblems` (narrative warnings): ≤ 30 characters before the suffix, one
      question, a stake or surprise word, a number (curio and story; 原來如此 only where useful per
      its refresh SPEC), no calm reading question, the point inside the first 18 characters, the
      thumbnail headline not repeating the title.
- [x] 原來如此 writer prompt carries the 黑猫 title formula.
- [x] Retitle batches under docs/videos/packaging-refresh-20261111/ (zh-TW + 8 locales, fixed series
      suffixes), applied by the owner in Studio or by `video-youtube-caption-titles --set-title --apply`
      on the host with the owner's explicit OK. No video.json or i18n file is edited (that would stale
      the translations and the publish approval).

## Notes

- 59 episodes retitled (curio 41, story 15, 原來如此 T27 + QR Code); every zh-TW title passes
  `titleProblems`, every locale title fits 100 characters with the caption tag, every figure is in
  that episode's script or claims. The lead corrected Kincho (the proposal set two different products
  as 早年／如今).
- Found on the way: several live titles differ from video.json (check Studio first); s11 is in a
  Studio thumbnail test since 2026-11-11; some i18n files use pre-2026-11-13 series names; Zippo short
  names 奇聞檔案局 (filed 2026-11-19-zippo-short-wrong-series-subscribe-line).
- A browser review of 黑猫研究院's top ten (asked of a local session, the cloud IP gets LOGIN_REQUIRED)
  may adjust the formula; a later PR revises the sheets then.

## How to verify

```bash
node --test tools/video/core/narrative.test.mjs tools/video/automation/explainer-series.test.mjs
```
