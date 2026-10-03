---
id: 2026-10-03-illustrated-slides-round-2-a-family
title: Illustrated slides round 2: a family of print looks, a style anchor per video, a sharper craft judge and lighting variety
status: in-progress
priority: P2
area: tools
owner: claude-fable-5-1-illustration-round2
claimed_at: 2026-10-03T08:25:14Z
created_at: 2026-10-03T08:24:18Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/drama.mjs
  - tools/video/core/drama.test.mjs
  - tools/video/core/fixtures/illustrated
  - tools/video/media/keyframes.mjs
  - tools/video/media/look-keyframes.test.mjs
  - tools/video/media/stages.mjs
  - tools/video/media/stages.test.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
  - apps/api/app/video_media/providers
  - apps/api/tests
  - docs/videos/ILLUSTRATED.md
  - .agents/skills/youtube-video/references
  - .claude/skills/youtube-video/references
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Illustrated slides round 2: a family of print looks, a style anchor per video, a sharper craft judge and lighting variety

## Why

On 2026-10-03, after PR #1166 shipped, the owner said again that the videos and the illustrated
slides' pictures look too much like AI and must get better. Production had not drawn a single
illustrated picture since the deploy (automatic drafts off, seven slides videos blocked on the
slides switch), so samples were drawn through the production media server from this machine:
the `tech-story` look comes out as a clean children's-book digital comic (an even outline around
everything, one cute face), which is what a viewer reads as a machine; a print's halftone grain,
overprint and off-register inks read as a hand; "full-bleed, edge to edge" makes the model paint
a paper margin; and a drawn picture sent back as a `style` reference keeps the technique across
pictures without copying the scene. Design and samples: `docs/videos/ILLUSTRATED.md` §第二輪.

## Definition of done

- [x] Five print looks in `core/drama.mjs` (`SLIDES_PRESETS`: four risograph ink pairs and a
      linocut), chosen per video by slug (`slidesPresetFor`) in `settle()` when the writer names
      none; `tech-story` stays for a video that names it; the negatives refuse borders and bars.
- [x] `keyframes` draws one style plate per illustrated video first (`keyframes/plate.json`,
      bound to `look_hash`), sends it with every shot as a `style` reference and to the judge as
      "style plate"; a prompt edit keeps the plate, a new look redraws it; owner style frames
      replace it; the dry-run counts and prices it.
- [x] The Gemini image provider tells the model the last reference is a style plate (technique,
      not scene) and says "keep every character" only for character sheets.
- [x] The judge's `craft` and `clean` questions name the AI tells (even outline, uniform detail,
      rendered finish; bars, borders, margins), each at most 400 characters.
- [x] The writer's guide asks for a day of light, people acting on each other, a thing in hands,
      a joke now and then, and leaves `look` to the worker; lint warns when more than half the
      pictures are at night or under a lamp.
- [x] Docs and skill: `ILLUSTRATED.md` §第二輪, `visuals.md`, `writer-video.md`, `automated.md`.

## Steps

- [x] Samples: baseline, four candidates, one plated set (`mokaair-work/videos/_audition/look-20261003/`).
- [x] Presets, `slidesPresetFor`, `settle()`, prompts, lint heuristics, tests.
- [x] Style plate in `keyframes.mjs`, provider text, tests.
- [ ] Long-form receipt rebound by an independent reviewer (`docs/videos/long-form/review.*`).
- [ ] After deploy: the first illustrated video's plate and contact sheet, craft scores, cost.

## How to verify

```bash
node --test tools/video/core/drama.test.mjs tools/video/media/look-keyframes.test.mjs tools/video/media/stages.test.mjs tools/video/automation/prompts.test.mjs tools/video/automation/automation.test.mjs
cd apps/api && uv run pytest tests/test_video_media_providers.py -q
node tools/video/long-form/cli.mjs check
```

## Notes

- Judge scores on the samples (threshold 7): tech-story 5.4–7.0, riso 6.5–7.0, gouache 6.5–6.9,
  linocut 6.0–6.7, plated riso 6.5–6.6; `craft` sits at 6–7 for every look, so the judge alone
  does not separate them; the eye does. Three seeds pass about one picture in three; the plate
  keeps the best take even when none passes.
- The plate test ran against the server's old reference text ("keep every character"); it still
  kept the technique and did not copy the scene. The new text is in this PR and needs the API
  image deployed.
- `pen-and-watercolour sketchbook` looked the most hand-made but the model draws an open
  notebook with page edges and writes prices on signs; not in the rotation.
- The plate is not on the contact sheet (`review/sync.mjs` pages by shot count).
- Seven slides videos on production are blocked with "pictures for slides videos are off" from
  before the owner re-saved the settings; the owner has to retry them on /admin/videos.
