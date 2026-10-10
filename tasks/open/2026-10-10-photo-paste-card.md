---
id: 2026-10-10-photo-paste-card
title: Slides: a photo card that pastes a real photograph on the series ground with its credit
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-10T16:20:00Z
completed_at:
branch:
depends_on:
scope:
  - tools/video/templates/templates.mjs
  - tools/video/templates/theme.css
  - tools/video/templates/templates.test.mjs
  - tools/video/templates/fixtures/showcase/video.json
  - tools/video/render/plan.mjs
  - tools/video/core/lint.mjs
  - docs/videos/README.md
  - docs/videos/ILLUSTRATED.md
---

# Slides: a photo card that pastes a real photograph on the series ground with its credit

## Why

The owner's history-and-curiosity series (docs/videos/history-curiosity/README.md §照片) and,
from 2026-10-10, So That's Why may put real photographs in a video: public-domain archive
pictures (Wikimedia Commons, NASA, national archives), stock photos (Pexels, Pixabay, already
fetched by `stock fetch`) and the owner's own screenshots. The reference channel (馬臉姐) shows
them as cut-outs pasted beside the presenter. We have no presenter, and the only template that
takes a photograph today is `screenshot`: a full-bleed capture with an optional focus box and
a credit capsule, which reads as a screenshot, not a photograph.

## Definition of done

- [ ] A `photo` template: `data.image` (a repo path or `stock/<sha256>.<ext>`, the rules of
      `screenshot`), `data.caption?` (one line, ≤ 40 characters, card text), `data.credit?`
      (≤ 60 characters, the capsule), `data.tilt?` (−3 to 3 degrees; by the scene id when
      absent, alternating sign). The photograph sits on the theme ground like a print: a 24 px
      white border, the tilt, a soft shadow, 70–80 % of the frame's height, centred right; the
      caption at the left or below, never burned into the photograph; the credit capsule at the
      photograph's lower right. Portrait and square photographs fit by height.
- [ ] `renderProblems` holds a `photo` scene to the `screenshot` rules: the file exists in the
      work directory and `assets[]` names the same path (so the description carries the
      credit); lint checks the fields' shapes.
- [ ] The render plan hashes the photograph's bytes into the scene's key as it does for
      `screenshot`, so a swapped file redraws one scene.
- [ ] The showcase fixture has a `photo` scene; `docs/videos/README.md` §版型 lists it;
      `docs/videos/ILLUSTRATED.md` §圖庫照片 says a stock photo may go on a `photo` card.
- [ ] Assemble treats it as a single-state card (drift or push-in like `big`), nothing new.

## Steps

- [ ] Read `tools/video/templates/templates.mjs` (`screenshot`'s spec and HTML), `theme.css`
      (`.screenshot`, the credit capsule's CSS that rides only with a credit), `render/plan.mjs`
      (how `workdir` and `stock/` paths enter the key).
- [ ] Add the spec, HTML and CSS; keep the credit capsule's CSS shared with `screenshot`.
- [ ] Tests: the spec's limits, a render-plan key that changes with the bytes, the lint
      refusals; `npm run test:tools` on the touched files.

## How to verify

`node tools/video/cli.mjs render --slug <a video with a photo scene>` draws the card; the PNG
shows the border, tilt, shadow and capsule; the description composed by `package` lists the
photograph under 📷 圖片來源; `node --test tools/video/templates/templates.test.mjs` passes.

## Notes

- 2026-10-10 filed from the history-and-curiosity plan. Until it lands, `screenshot` with
  `data.credit` is the stopgap.
- Keep the picture inside the centre of the frame: a Short cut from a 16:9 slide keeps only the
  middle 32 % of its width (`shorts/motion.mjs`).
