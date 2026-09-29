---
id: 2026-09-29-video-lint-translated-descriptions-over-5
title: Video lint: translated descriptions over 5,000 bytes and ja/ko inner-zero numbers; thumbnail text over the brand mark
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-29T02:57:08Z
created_at: 2026-09-29T02:56:56Z
completed_at: 2026-09-29T02:57:18Z
branch:
depends_on: []
scope:
  - docs/videos/DUBS.md
---

# Video lint: translated descriptions over 5,000 bytes and ja/ko inner-zero numbers; thumbnail text over the brand mark

## Why

Videos 5 and 6 of the English AI season (2026-09-28) hit three problems that only showed up late:

- The Japanese and Korean descriptions of `rtx-spark-local-ai` composed to 5,365 and 5,141 bytes
  (Hangul and kana are 3 bytes each). `package` would have refused them, but `lint` only composed
  the zh-TW description, so a caption reviewer found it by hand.
- The Japanese and Korean dub voices read 4050億 and 4050억 as 450. Local Whisper and Gemini both
  heard 450. Writing 4千50億 and 4천50억 was read right.
- A thumbnail variant's small line wrapped to two lines and ran into the MOKAAIR mark. The render
  check only compares the content box with its area, and the brand sits outside the flow, so
  nothing was reported.

## Definition of done

- [x] `lint` composes every translation's description like `package` does (article link, chapters,
      sources, hashtags) and warns when YouTube would refuse it; the zh-TW description now counts
      its hashtags too.
- [x] `lint` warns on ja and ko lines with a number that has a zero inside it before 億, 万, 억 or 만,
      and says how to write it.
- [x] Rendering reports thumbnail text that overlaps the brand mark.
- [x] `docs/videos/DUBS.md` lists the voice traps found on videos 5 and 6 and how each was fixed.

## Steps

- [x] `tools/video/core/lint.mjs` and two tests in `lint.test.mjs`; both fail on the old lint.
- [x] `tools/video/render/browser.mjs` `layoutProblems`: brand overlap check.
- [x] DUBS.md section 「聲音會唸錯的地方」.

## How to verify

```bash
npm run test:tools
node tools/video/assemble/smoke.mjs --workdir <tmp>
node tools/video/assemble/smoke.mjs --fixture drama --workdir <tmp>
```

## Notes

- The six season videos lint without any new warning; the rules were checked against what they
  would have caught: RTX ja/ko before their review fixes, and 4050億 in RTX pt7g and 6p8h.
- The thumbnail check was confirmed on the two-line variant (flagged) and its one-line fix (clean);
  cached frames are not re-checked until they are drawn again.
- Tag crowding (one 500-character tag list per video, filled in locale order) is described in
  DUBS.md but not linted; a warning when a locale keeps none of its tags would be a small follow-up.
