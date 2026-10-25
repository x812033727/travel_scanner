---
id: 2026-10-24-story-series-thumbnails-take-the-bold
title: Story-series thumbnails take the bold look of the high-view channels (bright ground, two-line outlined headline, the thing itself)
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-24T16:49:13Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/templates/theme.css
  - tools/video/templates/templates.mjs
  - tools/video/qa/thumbnail.mjs
  - docs/videos/BRANDING.md
---

# Story-series thumbnails take the bold look of the high-view channels (bright ground, two-line outlined headline, the thing itself)

## Why

2026-10-25 the owner asked why 奇聞檔案局 and 品牌故事 get 0–7 views while the channels they were
modelled on get hundreds of thousands (report: `docs/videos/channel-review-20261025-story-series/README.md`).
Side by side, the thumbnails are the most visible gap. The reference channels (黑猫研究院 Seiko,
A4, Dolby; 馬臉姐; cheap) share one look: a bright, saturated ground; two lines of yellow or white
text with a black outline, a 6–8 character headline and an 8–12 character second line; the thing
itself as the subject (the watch, the Michelin man, an A4 sheet, the Dolby mark) or a face with an
exaggerated expression. Ours (`thumb` template, `tools/video/templates/theme.css` `.thumb`) are a
dark teal ground, a 136 px six-character headline, a label pill, a muted MiniMax illustration with
no expression close-up and a small MOKAAIR mark. At list size they read as one dark rectangle.

## Definition of done

- [x] The owner has seen three sample thumbnails of delivered episodes (H01 v2, S01, H12) in the
      bold look (2026-10-25, the session's scratchpad `thumb/bold-sheet.jpg`) and said to try it.
- [x] A `thumb` layout for `curio-` and `story-` videos (`THUMB_BOLD_LAYOUT`, layout d): full-bleed
      keyframe under a bottom scrim, headline yellow and second line white, both outlined, no
      label pill, the brand mark small; the default for the two slug prefixes, a choice elsewhere.
- [ ] `qa/thumbnail.mjs` adds the second line's limit (about 12 characters) and checks the bold
      headline's size at 320 px with layout d's full width, not the 40% column's.
- [ ] `docs/videos/BRANDING.md` records the look; a rendered episode's thumbnail viewed next to a
      reference at list size.

## Steps

- [x] Samples sent to the owner (brand stories: the company name stays as the owner decided on 2026-10-18).
- [x] Layout d in `templates.mjs`/`theme.css`, keyed by the two slug prefixes, outside the rotation.
- [ ] Extend the QA checks (second line, full-width headline estimate) and BRANDING.md.

## How to verify

`node --test tools/video/templates/templates.test.mjs tools/video/qa/thumbnail.test.mjs`; render a
curio episode's thumbnail (`node tools/video/cli.mjs render --slug curio-h01-v2`) and view it at
320 px wide next to a reference thumbnail.

## Notes

- 2026-10-25: layout d landed with the channel-review PR (branch
  `claude/quirky-files-content-review-27bf04`); what is left is the QA estimate and the doc.

- 2026-10-25 filed from the story-series channel review. The open task
  `2026-10-11-curio-series-own-intro-thumbnail-shorts` is about a series identity (intro, Shorts
  theme); this one is only the thumbnail look and should land first.
- The reference thumbnails viewed on 2026-10-25 (ids a7NlBfRCgqI, cP_Y9n23cmQ, ni-loGxhkgs,
  cbTaGjK-YQE, hbTsNpCg5N4) are not reused: the look is copied, never the pictures.
