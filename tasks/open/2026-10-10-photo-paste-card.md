---
id: 2026-10-10-photo-paste-card
title: Slides: a photo card that pastes a real photograph on the series ground with its credit
status: review
priority: P3
area: tools
owner: claude-opus-photo-card
claimed_at: 2026-10-10T11:13:20Z
created_at: 2026-10-10T16:20:00Z
completed_at:
branch: claude/photo-paste-card
depends_on: []
scope:
  - tools/video/templates/templates.mjs
  - tools/video/templates/theme.css
  - tools/video/templates/templates.test.mjs
  - tools/video/templates/fixtures/showcase/video.json
  - tools/video/render/plan.mjs
  - tools/video/core/lint.mjs
  - docs/videos/README.md
  - docs/videos/ILLUSTRATED.md
  - docs/videos/history-curiosity/look.md
  - tools/video/core/schema.mjs
  - tools/video/render/render.test.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/automation.test.mjs
  - tools/video/media/stock.mjs
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

- [x] A `photo` template: `data.image` (a repo path or `stock/<sha256>.<ext>`, the rules of
      `screenshot`), `data.caption?` (one line, ≤ 40 characters, card text), `data.credit?`
      (≤ 60 characters, the capsule), `data.tilt?` (−3 to 3 degrees; by the scene id when
      absent, alternating sign). The photograph sits on the theme ground like a print: a 24 px
      white border, the tilt, a soft shadow, 70–80 % of the frame's height, centred right; the
      caption at the left or below, never burned into the photograph; the credit capsule at the
      photograph's lower right. Portrait and square photographs fit by height.
- [x] `renderProblems` holds a `photo` scene to the `screenshot` rules: the file exists in the
      work directory and `assets[]` names the same path (so the description carries the
      credit); lint checks the fields' shapes.
- [x] The render plan hashes the photograph's bytes into the scene's key as it does for
      `screenshot`, so a swapped file redraws one scene.
- [x] The showcase fixture has a `photo` scene; `docs/videos/README.md` §版型 lists it;
      `docs/videos/ILLUSTRATED.md` §圖庫照片 says a stock photo may go on a `photo` card.
- [x] Assemble treats it as a single-state card (drift or push-in like `big`), nothing new.

## Steps

- [x] Read `tools/video/templates/templates.mjs` (`screenshot`'s spec and HTML), `theme.css`
      (`.screenshot`, the credit capsule's CSS that rides only with a credit), `render/plan.mjs`
      (how `workdir` and `stock/` paths enter the key).
- [x] Add the spec, HTML and CSS; keep the credit capsule's CSS shared with `screenshot`.
- [x] Tests: the spec's limits, a render-plan key that changes with the bytes, the lint
      refusals; `npm run test:tools` on the touched files.

## How to verify

`node tools/video/cli.mjs render --slug <a video with a photo scene>` draws the card; the PNG
shows the border, tilt, shadow and capsule; the description composed by `package` lists the
photograph under 📷 圖片來源; `node --test tools/video/templates/templates.test.mjs` passes.

## Notes

- 2026-10-10 filed from the history-and-curiosity plan. Until it lands, `screenshot` with
  `data.credit` is the stopgap.
- 2026-10-10 (claude-opus-photo-card) built on `claude/photo-paste-card`. What was decided, and
  where it departs from the wording above:
  - **Claimed with `--force`.** The tool refused because `2026-10-09-video-languages-are-four-drop-zh`
    still reads in-progress with all of `tools/video` in its scope; its work merged as #1413 on
    2026-10-10 and its branch is gone, so nothing there is being changed. That file was left as it
    is for its owner to close.
  - **Scope grew by six paths**: `core/schema.mjs` (the `TEMPLATES` list that validation reads),
    `render/render.test.mjs` (the render-plan tests, and one existing test that replaced
    `assets[]`), `automation/prompts.mjs` and its test (below), `media/stock.mjs` (the hint
    `stock fetch` prints now names the photo card), and `history-curiosity/look.md`.
    `theme.css` and `core/lint.mjs` are in the scope and were not touched: all the card's CSS
    rides in its own page (`TEMPLATE_CSS.photo`), and lint already checks every template's
    fields through `TEMPLATE_SPECS`.
  - **Layout**: the print is centred, not centred right, with the caption under it. A print is
    756 px tall with its border (70 % of the frame) without a caption and 700 px (65 %) with one:
    the chapter label above and YouTube's bottom 12 % below leave 808 px, and a tilted print needs
    room for its corners. A caption beside the print would have pushed the photograph out of the
    middle third a Short keeps, and left a 16:9 photograph a 340 px column for its caption.
  - **Tilt**: `data.tilt`, else by the scene id's hash: ±1.5°, ±2° or ±2.5°. "Alternating" is by
    hash, not by position, so adding a photo scene never turns the later ones the other way
    (which would also redraw them).
  - **assets[]**: a photo card's photograph must be listed wherever its file is (a repository
    path too); a screenshot's repository path still needs no entry, as before.
  - **The entrance** animates a mount around the print: `.enter` ends on `transform: none`,
    which would straighten a print it animated.
  - **The credit capsule** shares its CSS with `screenshot` through one function; the
    screenshot's bytes are unchanged (a test pins the whole string). On a portrait narrower than
    its credit the capsule runs out over the print's left edge instead of being cut to "圖：Wiki…".
  - **The worker's writer does not get the card**: `references()` hands it the showcase without
    the photo scene and without `assets[]` (`workerShowcase`), and no writer prompt names it.
    `docs/videos/README.md`, which the writer also reads, now lists `photo` in the template
    table (as it lists diagram and screenshot, which the prompt forbids by name); if the writer
    uses it anyway, lint takes the shape and render refuses the missing `assets[]` entry. The
    explainer-route ticket decides the prompt wording.
  - **Verified**: the showcase's other 17 scenes and its three thumbnails keep their keys and
    their HTML against `origin/main` (compared with the repository as root); the card was drawn
    with Edge and looked at in five shapes (4:3 painting, narrow portrait, tall newspaper column,
    16:10 page at −3° with a 40-character caption and a 60-character credit, a bare small scan
    scaled up).
  - **Not done here**: `node tools/video/cli.mjs render --file …/showcase/video.json` (How to
    verify, and `docs/videos/README.md` §改主題顏色或版型) is refused by the eight-minute floor on
    `origin/main` already ("starts at 0.5 minutes"); the card was drawn through `renderPlan` and
    `openRenderer` directly. `docs/videos/history-curiosity/README.md` §照片 still says
    "先用它頂著": PR #1415 has that file open. The skill's `automated.md` still says 16 templates
    (the automated route has 16). `docs/videos/README.md` and `core/schema.mjs` are bound by the
    long-form duration receipt, which is stale until an independent reviewer renews it.
- Keep the picture inside the centre of the frame: a Short cut from a 16:9 slide keeps only the
  middle 32 % of its width (`shorts/motion.mjs`).
