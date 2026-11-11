---
id: 2026-11-11-bright-explainer-and-drama-thumbnails
title: Thumbnails: So That's Why on a bright ground, AI dramas full-frame face with a coloured drama strip
status: review
priority: P2
area: tools
owner: claude-opus-5-5-thumbs-bright
claimed_at: 2026-11-11T12:50:14Z
created_at: 2026-11-11T12:49:54Z
completed_at:
branch: claude/keen-clarke-dg372g
depends_on: []
scope:
  - tools/video/templates/templates.mjs
  - tools/video/templates/templates.test.mjs
  - tools/video/render/plan.mjs
  - tools/video/qa/thumbnail.mjs
  - tools/video/qa/thumbnail.test.mjs
  - tools/video/core/explainer-cute.test.mjs
  - docs/videos/so-thats-why/thumbnails.md
  - docs/videos/thumbnail-looks-20261111
---

# Thumbnails: So That's Why on a bright ground, AI dramas full-frame face with a coloured drama strip

## Why

2026-11-11 the owner reviewed the channel's three remaining series (奇聞檔案局, 原來如此事務所, AI 劇)
and asked to see sample thumbnails. Two of the three still drew the old look:

- 原來如此 put an ink-navy scrim over the keyframe with cream type; the 2026-11-01 refresh
  (`docs/videos/so-thats-why/refresh-20261101/SPEC.md`) had already asked for 亮底、高對比 but the code
  never switched.
- AI dramas (種田娶妻打天下, 恁祖媽今年18) had no look of their own: the channel's rotation (text
  column left 40%, picture right 60%, one of four dark tones by slug), so every episode looked
  different and the face was small. `drama-craft.md` measured the reference dramas: 15 of the 16
  most viewed thumbnails are a face filling the frame, 14 carry a 4–8 character title in the
  bottom third.

The owner saw three samples (P14, 種田 e003, 祖媽 e018) and said: 「我怎麼覺得你做的縮圖比較好，幫我用這樣的模式開PR」.

## Definition of done

- [x] So That's Why thumbnails render on a bright ground (cream scrim over a keyframe, sky-to-sunset
      gradient without one), ink-navy headline outlined in white, mustard emphasis, sub line on an
      ink-navy plate, stamp kept.
- [x] An AI drama (drama format, not an explainer preset, not curio-/story-) takes the new layout
      `f` unless `data.layout` names another: full-frame keyframe, yellow outlined headline in the
      bottom third, the drama's name as a strip in the drama's colour (種田 orange, 祖媽 red, other
      dramas a palette colour by slug, or `data.accent`).
- [x] QA measures the bright series headline at its new 150 px and a layout `f` headline across
      the frame with an 8-character cap.
- [ ] The owner looks at the first real episode thumbnails drawn after merge.

## Steps

- [x] `templates.mjs`: `THUMB_DRAMA_LAYOUT`, `isDramaThumbDoc`, `dramaAccent`, `THUMB_DRAMA_CSS`, bright `THUMB_SERIES_CSS.sothatswhy`, `data.accent` validation.
- [x] `render/plan.mjs` passes `drama: isDramaThumbDoc(doc)`.
- [x] `qa/thumbnail.mjs`: `HEADLINE_SERIES` at 150 px, `HEADLINE_DRAMA`, `DRAMA_HEADLINE_MAX`.
- [x] Tests updated; `docs/videos/so-thats-why/thumbnails.md` says the code switched.
- [ ] Follow-up: `qa/cli.mjs` still passes only `data.layout`, so a drama that takes layout `f`
      by default is measured with the channel's column rule (as before this change). Passing the
      resolved layout needs `tools/video/qa/cli.mjs`, which the independent duration review binds
      by hash (`tools/video/long-form/review.test.mjs`); change it together with a new review.

## How to verify

```bash
node --test tools/video/templates/*.test.mjs tools/video/qa/*.test.mjs tools/video/render/*.test.mjs tools/video/core/*.test.mjs tools/video/long-form/review.test.mjs
```

Render any 種田 or 祖媽 episode and any `sothatswhy-` episode and look at `thumbnail.png`.

## Notes

- The claim was forced over four overlapping claims on `templates.mjs`/`qa/thumbnail.mjs`, all
  10+ days stale (2026-10-14 to 2026-11-01) with no activity.
- Layout and CSS are not in the visual hash, so approved storyboards and cuts stay valid; the
  thumbnail key follows the HTML, so the next render redraws the thumbnail in the new look.
- Second pass (edge cases rendered through the real renderer): the stamp at the column's top
  right covered a 5-character first line, every English headline, and the picture under
  `subject: "right"`, so it moved beside the series' name at the bottom left (112 px); the column
  keeps 160 px clear at the bottom, the headline box is two lines (330 px, `SERIES_THUMB_HEADLINE`),
  and the sub line stays on one line (fitText shrinks it) — before, a two-line sub plate ran into
  the series' name and the renderer reported it. Drama headlines use `text-wrap: balance`, so seven
  characters break 3+4, not 5+2.
- Third pass (owner: 「AI劇的字跟圖解決一下，是不是AI劇就不要字?」): kept the text (14 of 16 reference
  thumbnails carry it) but held it to one line at 170 px that shrinks instead of wrapping, the
  picture anchored at 18% from the top and the shade starting lower, so the headline never climbs
  onto the face. `DRAMA_THUMB_HEADLINE.maxLines` is 1 and qa measures one line.
- 種田 e003's chosen keyframe has a calm face; the look needs the most expressive shot — pick
  `data.shot` for the face, not the scene.
