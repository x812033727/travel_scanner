---
id: 2026-10-03-illustrated-slides-lint-heuristics-the-shorts
title: Illustrated slides lint heuristics, the Shorts crop figure and an end-to-end 2K test
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-03T04:27:39Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/drama.mjs
  - tools/video/core/drama.test.mjs
  - tools/video/core/fixtures/illustrated
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/media/stages.mjs
  - tools/video/media/stages.test.mjs
  - tools/video/shorts/motion.mjs
  - docs/videos/SHORTS.md
---

# Illustrated slides lint heuristics, the Shorts crop figure and an end-to-end 2K test

## Why

PR #1166 gave illustrated slides a picture-variety lint, a 2K keyframe path and a corrected
Shorts crop figure. A re-check of its fix commit after it was green found only low-severity
leftovers, none of which blocked the merge. They are warnings a writer is not forced to act on,
a comment and a document that still carry the old number, and one path no test drives end to
end. Left alone they make the lint a little noisier and less trustworthy than it should be.

## Definition of done

- [ ] `SHOT_SIZE` in `tools/video/core/drama.mjs` accepts the usual spellings of the sizes the
      guide names ("low-angle", "high-angle", "bird's eye", "top down", "over-the-shoulder") and
      no longer passes a prompt on an incidental adjective ("a medium bowl", "over medium heat",
      "a wide street"): match a size as a size (at the start of the prompt, or followed by
      shot / view / angle / of).
- [ ] `LOOK_WORDS` does not read dairy cream as the palette ("ice-cream", "whipped cream",
      "cream poured into coffee").
- [ ] `motifOf` folds -ies / -ves / -oes / -ses plurals and short -xes plurals ("boxes"), so a
      prop written in both numbers counts once.
- [ ] The three-in-a-row error names the field that actually carries the move (`data.motion`
      when the camera word names none) and does not suggest "drift" as a fix when the run comes
      from motion prompts.
- [ ] `tools/video/shorts/motion.mjs` (the comment on `backgroundChain`) and `docs/videos/SHORTS.md`
      say a Short keeps the middle 32% of a 16:9 keyframe, not 56%.
- [ ] The example's `race` shot keeps its subject in the middle third (two runners far apart
      under a pan is what the guide now forbids).
- [ ] `look-keyframes.test.mjs` drives `keyframes` once with a status whose slides choice carries
      `usd_per_image_2k` (requests carry `size: "2K"`, the dry-run prints `pictures at 2K` and the
      2K price, a drama under the same status stays at 1K) and pins the explainer's rubric
      (no `craft`).
- [ ] `choiceFor` in `tools/video/media/stages.mjs` reads `status.slides_enabled`: with the slides
      switch off the server draws a slides video with the drama's model, so the tool must size
      and price with that choice, not with `slides_image`.

## Steps

- [ ] Patterns and helper in `core/drama.mjs`, with a table-driven test in `drama.test.mjs`.
- [ ] `choiceFor` and its tests; the end-to-end 2K test.
- [ ] The two 56% mentions; the `race` prompt.
- [ ] The bound files this touches (`core/drama.mjs`, `core/drama.test.mjs`,
      `media/look-keyframes.test.mjs`) need the long-form duration receipt rebound by an
      independent reviewer (`docs/videos/long-form/review.*`).

## How to verify

```bash
node --test tools/video/core/drama.test.mjs tools/video/media/look-keyframes.test.mjs tools/video/media/stages.test.mjs tools/video/shorts/motion.test.mjs
node tools/video/long-form/cli.mjs check
```

## Notes

- Production on 2026-10-03: `slides_enabled` is false and the drama model is gemini-3-pro-image,
  so a slides video today is drawn by Pro at 2K (same price as its 1K); the tool's estimate uses
  Flash's 2K price. The ledger books what the server charged, so only the estimate is off.
- `tools/video/shorts/` was in the scope of `2026-09-28-sothatswhy-shorts-from-episode` (a stale
  claim) when PR #1166 was written, which is why the comment there was left.
