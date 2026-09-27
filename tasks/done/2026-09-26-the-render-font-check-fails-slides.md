---
id: 2026-09-26-the-render-font-check-fails-slides
title: The render font check fails slides whose only use of a subset overlaps another, and clipped code passes
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-26T01:52:54Z
created_at: 2026-09-26T01:52:35Z
completed_at: 2026-09-26T02:27:54Z
branch: claude/video-render-font-check
depends_on: []
scope:
  - tools/video/render/browser.mjs
---

# The render font check fails slides whose only use of a subset overlaps another

## Why

On 2026-09-26, `render` refused four slides of batch 2 with "the slide font did not load for
all of its text":

- `gemini-student-offer`: `official-chapter`, `four-gates-diagram` and `real-math-big`;
- `ai-agent-permissions`: `event-one-diagram`.

A redraw with `--force` gave the same result. The frames themselves were right.

Listing the failing characters per weight showed where the check goes wrong:

| Slide | Weight | Characters |
| --- | --- | --- |
| `official-chapter` | 700 | `MOKAIR` |
| `official-chapter` | 850 | `02` |
| `real-math-big` | 900 and 450 | `$` |
| diagram slides | 450 | 「核」 and 「擴」 |

- **What the browser loads.** To draw a character, it loads one of the `@font-face` subsets whose
  `unicode-range` holds that character.
- **What the check wants.** `document.fonts.check()` wants every face that covers the text to be
  loaded.
- **Why they disagree.** fontsource's Noto Sans TC slices overlap the Latin subset and each other.
- **Why only these slides.** On a slide where no other text pulls in the second face, the check
  fails though nothing fell back.
- **A second flaw.** The check also asked for weight 400 for all text, while chapter numbers and
  big numbers are drawn only in heavy weights.

### The code panel clipped lines without a word

The same batch showed a second gap in the render's layout check. In `gemini-student-offer`,
the `demo-code` slide had 13 lines, and its panel shows 9 at 34 px. Lines 10 to 13, the whole
prompt, were cut off. `.t-code .panel` has `overflow: hidden`, so the content box above it
never overflowed and nothing was reported. The template's static check still says "at most
16 fit". The panel's real capacity depends on the title and caption, so the renderer now checks
what shows: each line's bottom against the panel's.

## Definition of done

- [x] A code slide whose panel does not show every line fails `render` with "the code panel shows
      N of M lines; shorten the code".

- [x] Before the check, every face of the slide font that covers the slide's text is loaded, per
      weight and style as drawn (`document.fonts.load`). A face that really cannot load is still
      reported: `load()` rejects for it.
- [x] The check runs per weight and style. It names the characters that are not loaded, so the
      next failure says what to look at.

## Steps

- [x] `loadFaces` runs in the page after `document.fonts.ready`. `layoutProblems` groups text by
      computed weight and style.

## How to verify

- Before the change, `node tools/video/cli.mjs render --slug gemini-student-offer --channel msedge
  --force` failed on the three slides. After it, the render passes (37 states), and so does
  `ai-agent-permissions` (33 states).
- The old 13-line `demo-code`, rendered under a throwaway slug, now fails with "the code panel
  shows 9 of 13 lines; shorten the code". The 9-line version passes.
- CI's `video-tooling.yml` smoke test still renders the minimal video.

## Notes

- Earlier I suspected the diagrams: they set `font-family` to Microsoft JhengHei first. That was
  not the cause. `theme.css` already forces the slide font on inline SVG with `!important`.
- The characters that fail depend on each slide's text, so the minimal fixture could only cover
  this by chance. The smoke test proves the new page function runs; the four batch 2 slides are
  what proved the fix.
