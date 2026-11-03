---
id: 2026-11-03-curio-thumbnails-and-titles-follow-the
title: Curio thumbnails and titles follow the 2026-11-03 YouTube review: famous name first, sub adds a fact, one big face on the right
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-curio-thumb-review
claimed_at: 2026-11-03T09:37:19Z
created_at: 2026-11-03T09:36:34Z
completed_at:
branch: claude/curio-thumb-review-20261103
depends_on: []
scope:
  - .agents/skills/curio-episode/SKILL.md
  - .claude/skills/curio-episode/SKILL.md
  - tools/video/automation/explainer-series.mjs
  - tools/video/automation/explainer-series.test.mjs
  - tools/video/qa/thumbnail.mjs
  - tools/video/qa/thumbnail.test.mjs
  - tools/video/qa/cli.mjs
  - docs/videos/long-form/review.json
  - docs/videos/long-form/review.md
---

# Curio thumbnails and titles follow the 2026-11-03 YouTube review: famous name first, sub adds a fact, one big face on the right

## Why

The channel's organic thumbnail CTR was 0.7–0.8% (YouTube Help says half of channels sit at
2–10%); nearly every view came from paid promotions. On 2026-11-03 six scheduled curio episodes
(curio-s02/s04/s05/s06/s09/s17-v2) got new titles (famous name first) and thumbnails redrawn by
hand with layout d: headline = the famous name + the reversal, sub = a hard fact, and a frame with
one big expressive face on the right. Old headlines (「史書裡沒有他」「早死了？11 年」「誰先上門？」)
named nobody and read as riddles. The owner wants new episodes drafted by the host worker to come
out this way without hand fixes.

## Definition of done

- [x] The curio skill's §標題與縮圖 and the host worker's curio thumbnail guide ask for: line 1 the
  famous name, line 2 (stressed) the reversal with a question mark; `sub` a fact the headline and
  the title do not say; `shot` one large face in the right 55% of the frame.
- [x] The owner's 2026-10-12 rule stays: every title ends with the locale's caption tag
  (`CAPTION_TAGS`, added by the tool).
- [x] qa warns when a curio headline is not name + reversal, and when `sub` repeats the title.

## Steps

- [x] Skill (and its `.claude/skills` mirror).
- [x] `explainer-series.mjs` MYSTERY `thumbnailGuide`.
- [x] `qa/thumbnail.mjs` warnings, `qa/cli.mjs` passes sub and slug, tests.

## How to verify

`npm run test:tools`, `node --test tools/video/qa/thumbnail.test.mjs`, and the automation tests.

## Notes

- Claimed with `--force`: the scope overlapped `2026-11-01-ai-series-thumbnails-ai101-look`
  (status review, its PR #1981 already merged) and `2026-10-26-qa-warns-when-a-long-video`
  (stale in-progress, no branch, nothing on main since).
- The curio guide lives in `tools/video/automation/explainer-series.mjs` (MYSTERY series), not in
  `prompts.mjs`; `prompts.mjs`'s `shotGuide` only splices `p.thumbnailGuide` / `p.titleGuide` in.
- Sources: YouTube Help CTR benchmark https://support.google.com/youtube/answer/7628154 , A/B test
  https://support.google.com/youtube/answer/16391400 , vidIQ face stats
  https://vidiq.com/blog/post/youtube-thumbnail-design-tips/ .
- Changing `thumbnailGuide` moves the pinned hashes of `writer:explainer-mystery` and
  `writer:discuss-mystery` (`explainer-series.test.mjs`). An unfinished curio writer journal on the
  host stops with `video_ai_receipt_input_changed` after deploy; restart that draft.
- The headline still counts at most 6 (「諸葛亮\n**沒出山？**」 is 6; the full-width ？ does not
  count). A two-character name with a three-character reversal stays under the title-repeat
  warning (ratio ≤ 0.5), so name-first titles and name-first headlines can coexist.
- `tools/video/qa/cli.mjs` is bound by the duration review receipt; the increment
  (reviewer `claude-pr-review-curio-thumb-20261103`, DURATION_ONLY PASS) is in
  `docs/videos/long-form/review.md`. The other Windows-local `test:tools` failures (backup, tts,
  adult_english, elementary) are in untouched files.
