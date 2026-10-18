---
id: 2026-10-18-story-thumbnail-brand
title: Brand story thumbnails show the company's name in large type (thumbnail.brand)
status: in-progress
priority: P1
area: tools
owner: claude-opus-5.5-story-thumb-brand
claimed_at: 2026-10-18T10:50:02Z
created_at: 2026-10-18T10:48:57Z
completed_at:
branch: claude/story-thumbnail-brand
depends_on: []
scope:
  - tools/video/templates/templates.mjs
  - tools/video/templates/templates.test.mjs
  - tools/video/story-plans/plan.mjs
  - tools/video/story-plans/plan.test.mjs
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
  - tools/video/core/timeline.mjs
  - apps/api/app/video_automation/stories.py
  - apps/api/tests/test_video_story.py
  - .agents/skills/youtube-video/references/story.md
---

# Brand story thumbnails show the company's name in large type (thumbnail.brand)

## Why

The owner (2026-10-18) found that a brand story's thumbnail never says which company it is
about: on `story-adapt-seiko-quartz-astron` the column shows an orange 「品牌故事」 tag, the
headline 「比車貴的錶」 and a cute illustration, and nothing says Seiko. He chose "大字品牌名":
the company's name in very large plain text in the channel's font in place of the tag. No logo
image, and no AI-drawn logo.

## Definition of done

- [x] A story plan may carry `thumbnail.brand` (optional, one line, at most 12 characters);
      `plan.mjs` and the API's import check (`stories.py`) accept it and reject a longer one.
- [x] A thumbnail with `data.brand` draws the name in place of the tag, set as large as the
      40% column allows (up to 168 px); without it the page is byte for byte the old one.
- [x] An already shot story can take a brand without re-buying anything: `visualHash` leaves
      `thumbnail.data.brand` out, and `references/story.md` §手動接手 says which files to edit
      and which commands redraw only the thumbnail.

## Steps

- [x] templates.mjs: `THUMB_BRAND_MAX`, `brandFontSize`, `brandProblem`, `.marque` CSS inline.
- [x] plan.mjs: problem past 12 characters, warning when the name is set below 96 px.
- [x] story.mjs `composeStory` passes `plan.thumbnail.brand` into `thumbnail.data.brand`.
- [x] stories.py `LIMITS["brand"]` and the check.
- [x] timeline.mjs `visualHash` without the brand.
- [x] Tests in all four places; previews in the PR description.

## How to verify

```bash
node --test tools/video/templates/templates.test.mjs tools/video/story-plans/plan.test.mjs tools/video/automation/story.test.mjs
cd apps/api && uv run pytest tests/test_video_story.py
```

## Notes

- `tools/video/core/timeline.mjs` is bound by the long-form duration review
  (`tools/video/long-form/review.mjs` REVIEW_FILES): `node tools/video/long-form/cli.mjs check`
  reports `stale duration review binding: tools/video/core/timeline.mjs` and
  `tools/video/long-form/review.test.mjs` fails until an independent agent records a
  DURATION_ONLY increment. Not rebound here on purpose.
- Changing `doc.thumbnail` in any other way still changes `visualHash`, which voids the
  keyframes and clips manifests of a drama (clips.mjs keeps no shot when the hash differs). That
  is why the brand is left out of it; the headline is not, so changing a shot story's headline
  makes its keyframes and clips stale (not tried on a real story). Worth its own task if that ever needs doing.
- Measured in Noto Sans TC 900: 「SEIKO」 at 120 px is 363 px wide, so a capital is about 0.62 em.
