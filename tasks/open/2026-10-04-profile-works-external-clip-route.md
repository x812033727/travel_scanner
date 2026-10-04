---
id: 2026-10-04-profile-works-external-clip-route
title: Production-profile works can take Hailuo or Kling clips through an approved external route
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-04T15:43:43Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/clips.mjs
  - tools/video/media/clips.test.mjs
  - tools/video/core/lint.mjs
  - docs/videos/series-plans/production-20261001/profile.json
  - docs/videos/DRAMA.md
---

# Production-profile works can take Hailuo or Kling clips through an approved external route

## Why

The owner wants the ten anime works (and later productions) made on Hailuo or Kling as well as
on the server. Today `clips import` (`tools/video/media/clips.mjs` `importClip`) refuses with exit 3
any project whose `series.production.profile` exists, whatever its provider or model, and
`productionClipSizeProblem` (`tools/video/core/lint.mjs`) requires a native 1920×1080 source, so a
Hailuo H3 2K clip (2560×1440) or a Kling 1080p clip cannot enter a profile-bound episode. Editing
the profile's provider or deleting the profile is not an approved workaround
(`.agents/skills/animation-production/references/browser-production.md` §1).

## Definition of done

- [ ] A profile can name approved external routes (for example `hailuo-web` H3 2K, `kling-web` 3.0 1080p) with their resolution and scaling rule, and `clips import` accepts a clip that matches one of them.
- [ ] A clip from a route the profile does not name is still refused with exit 3.
- [ ] The scaling a 2560×1440 source gets is decided and tested (downscale to 1920×1080 in assemble, or refuse); 720p or 768P upscales stay refused unless the owner approves them.
- [ ] The ten-work contract (`docs/videos/series-plans/production-20261001/profile.json`) records which routes the owner approved, with the date.

## Steps

- [ ] Ask the owner which routes and resolutions a profile may accept.
- [ ] Extend the profile contract and `importClip`; keep `productionClipProblems` checking provider, model and resolution per imported shot.
- [ ] Tests in `tools/video/media/clips.test.mjs` for accepted, refused and size cases.

## How to verify

```bash
node --test tools/video/media/clips.test.mjs tools/video/long-form/review.test.mjs
```

## Notes

- `tools/video/core/lint.mjs` and `tools/video/media/clips.test.mjs` are bound by SHA-256 in
  `docs/videos/long-form/review.json`; changing them needs an incremental review receipt (see the
  duration-receipt practice in the repo's review tooling). Plan that before editing.
- Filed from `2026-10-04-animation-preproduction-skill`; the owner chose "both" (new pilots now,
  profile works through a separate change).
