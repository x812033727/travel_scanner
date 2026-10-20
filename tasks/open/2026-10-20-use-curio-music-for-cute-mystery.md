---
id: 2026-10-20-use-curio-music-for-cute-mystery
title: Keep curio music and visual pacing in cute mystery brand stories
status: open
priority: P1
area: tools
owner:
claimed_at:
created_at: 2026-10-20T09:59:12Z
completed_at:
branch: codex/brand-stories-20261020
depends_on: []
scope:
  - tools/video/automation/story.mjs
  - tools/video/automation/story.test.mjs
---

# Keep curio music and visual pacing in cute mystery brand stories

## Why

The new brand-story batch uses the exact `cute-mystery` look and asks for the same music and illustration pacing as 奇聞檔案局. `composeStory` previously put its generic documentary prompt on every brand story. The preimage visual gate only recognized `story-five-` and two pilot slugs, so it would also let this batch pass with fewer than 70% illustrations or four consecutive cards. A production worker could therefore pay for media that violated the brief. Existing cute-mystery pilots must keep their original music prompt to avoid changing in-flight work.

## Definition of done

- [x] The exact `brand-stories-new-20261020` series with the exact `cute-mystery` look yields the shared `CURIO_MUSIC` prompt and gain/duck values.
- [x] Other brand stories, including existing cute-mystery pilots, keep `STORY_MUSIC`; `drama.music_enabled=false` omits music.
- [x] All five `story-new-20261020-*` slugs and later episodes in `brand-stories-new-20261020` get the exact-look, 70% illustration and at-most-three-card preimage gate.
- [x] Focused story tests pass, including an integrated chapter relint before keyframes.
- [ ] Change is reviewed and deployed to the production worker before this new series starts.

## Steps

- [x] Reuse `CURIO_MUSIC` in `composeStory` only for the new series with the exact look.
- [x] Extend `cuteStoryVisualProblems` to the new batch and its series; use slug or series identity so a wrong look cannot dodge the gate.
- [x] Add music and visual regression tests in `story.test.mjs`.
- [ ] Include this change in the same production release as the new story series.

## How to verify

`node --test tools/video/automation/story.test.mjs` (33/33 passed on 2026-10-20, including the series-identity case), `npm run check:tasks` and `git diff --check` passed. After deployment, inspect the first merged story's `video.json.music` before paid media: it should equal `CURIO_MUSIC` when music is enabled; a card-heavy script should return chapter lint errors before keyframes.

## Notes

`tools/video/automation/flow.mjs` already uses `CURIO_MUSIC` for the explainer curio preset. This change covers only the new brand-story series in the separate composer; no global music setting or existing pilot is altered. A later independent review found that an initial look-only branch would have affected existing cute-mystery pilots, so the branch is now restricted by both series slug and look. Claimed with `--force`: task-board still had overlapping `story.mjs` claims from 2026-10-17 and 2026-10-18, both beyond the documented 24-hour stale threshold. No tracked modifications were present before the first patch; changes touch only `story.mjs` and its test.
