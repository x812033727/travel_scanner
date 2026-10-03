---
id: 2026-10-03-illustrated-slides-lint-heuristics-the-shorts
title: Illustrated slides lint heuristics, the Shorts crop figure and an end-to-end 2K test
status: review
priority: P1
area: tools
owner: claude-fable-5-1-illustration-round2
claimed_at: 2026-10-03T08:24:13Z
created_at: 2026-10-03T04:27:39Z
completed_at:
branch: claude/video-production-tutorial-optimization-f5d1bc
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

- [x] `SHOT_SIZE` in `tools/video/core/drama.mjs` accepts the usual spellings of the sizes the
      guide names ("low-angle", "high-angle", "bird's eye", "top down", "over-the-shoulder") and
      no longer passes a prompt on an incidental adjective ("a medium bowl", "over medium heat",
      "a wide street"): match a size as a size (at the start of the prompt, or followed by
      shot / view / angle / of).
- [x] `LOOK_WORDS` does not read dairy cream as the palette ("ice-cream", "whipped cream",
      "cream poured into coffee").
- [x] `motifOf` folds -ies / -ves / -oes / -ses plurals and short -xes plurals ("boxes"), so a
      prop written in both numbers counts once.
- [x] The three-in-a-row error names the field that actually carries the move (`data.motion`
      when the camera word names none) and does not suggest "drift" as a fix when the run comes
      from motion prompts.
- [x] `tools/video/shorts/motion.mjs` (the comment on `backgroundChain`) and `docs/videos/SHORTS.md`
      say a Short keeps the middle 32% of a 16:9 keyframe, not 56%.
- [x] The example's `race` shot keeps its subject in the middle third (two runners far apart
      under a pan is what the guide now forbids).
- [x] `look-keyframes.test.mjs` drives `keyframes` once with a status whose slides choice carries
      `usd_per_image_2k` (requests carry `size: "2K"`, the dry-run prints `pictures at 2K` and the
      2K price, a drama under the same status stays at 1K) and pins the explainer's rubric
      (no `craft`).
- [x] `choiceFor` in `tools/video/media/stages.mjs` reads `status.slides_enabled`: with the slides
      switch off the server draws a slides video with the drama's model, so the tool must size
      and price with that choice, not with `slides_image`.

## Steps

- [x] Patterns and helper in `core/drama.mjs`, with a table-driven test in `drama.test.mjs`.
- [x] `choiceFor` and its tests; the end-to-end 2K test.
- [x] The two 56% mentions; the `race` prompt.
- [ ] The bound files this touches (`core/drama.mjs`, `core/drama.test.mjs`,
      `media/look-keyframes.test.mjs`) need the long-form duration receipt rebound by an
      independent reviewer (`docs/videos/long-form/review.*`).

## How to verify

```bash
node --test tools/video/core/drama.test.mjs tools/video/media/look-keyframes.test.mjs tools/video/media/stages.test.mjs tools/video/shorts/motion.test.mjs
node tools/video/long-form/cli.mjs check
```

## Notes

- **The `choiceFor` item is the urgent one.** Production on 2026-10-03 has `slides_enabled` false
  with the drama route on and gemini-3-pro-image as its model. The tool then expects the slides
  model (Flash) while the server draws with Pro, so `Stage.generate` books the first picture as
  failed with `video_media_model_changed` and stops the keyframes stage after one paid, unused
  picture. Every illustrated slides video is blocked there until the owner turns the slides
  switch on or this is fixed. The mismatch predates PR #1166 (it came with #983); asking for 2K
  did not cause it. With image-01 as the drama model the server answers 422 instead.
- `tools/video/shorts/` was in the scope of `2026-09-28-sothatswhy-shorts-from-episode` (a stale
  claim) when PR #1166 was written, which is why the comment there was left.
