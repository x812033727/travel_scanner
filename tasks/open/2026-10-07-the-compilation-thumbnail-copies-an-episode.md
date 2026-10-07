---
id: 2026-10-07-the-compilation-thumbnail-copies-an-episode
title: The compilation thumbnail copies an episode keyframe without checking its bytes
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T06:58:42Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/compilation.mjs
  - tools/video/automation/compilation.test.mjs
---

# The compilation thumbnail copies an episode keyframe without checking its bytes

## Why

A compilation's thumbnail sits on one of its episodes' keyframes. `tools/video/automation/compilation.mjs`
`planMetadata` copies the chosen episode keyframe to `keyframes/thumb-source.png` and writes the
compilation's `keyframes/manifest.json` with the sha256 **of that copy**. `thumbnailCandidates`
carries each candidate's `sha256` from the episode's manifest, but nothing compares it with the file.

So if an episode's selected keyframe file was drawn over by a later take, the copy takes the bytes
nobody approved and records them as the approved hash. Render's check
(`2026-10-07-the-thumbnail-is-drawn-from-a`, `render/cli.mjs` `changedBackgrounds`) then passes,
because the copy matches its own hash.

How the stale state is reached, from that ticket's review:
- Keyframe files are `keyframes/<shot>-<seed>.png`. A later run that draws the same seed again
  (after a prompt edit, or with `--force`) writes the take onto the selected file.
- The judge or a spend cap can then throw before the manifest is written.
- That leaves the old record with the old hash and `needs_review: false` over new bytes.
- A STOP marks the shot `needs_review`, which `thumbnailCandidates` already skips.

## Definition of done

- [ ] A candidate whose file is missing, has no recorded sha256, or hashes otherwise is never
  offered to the planner or copied.
- [ ] After the copy, the copy's hash is compared with the candidate's recorded one. The
  compilation manifest records that hash only if they match.

## Steps

- [ ] In `planMetadata`, filter `thumbnailCandidates(...)` by `existsSync(c.file)` and
  `(await sha256File(c.file)) === c.sha256`.
- [ ] After `copyFileSync`, compare `sha256File(THUMB_SOURCE)` with `chosen.sha256`. On a
  mismatch, remove the copy and drop `thumbnail.data.shot` or try again later.
- [ ] Tests in `compilation.test.mjs`: an episode keyframe drawn over is not chosen; the copy
  records the episode's hash.
- [ ] Optional: render's refusal text for a compilation says to plan the metadata again, not "run
  keyframes again". `keyframes` refuses a compilation, which has no drawn shots.

## How to verify

`node --test tools/video/automation/compilation.test.mjs tools/video/render/render.test.mjs`.

## Notes

- Found by the review of `2026-10-07-the-thumbnail-is-drawn-from-a` (2026-10-07). That review
  confirmed the gap is older than the render check and outside its scope.
