---
id: 2026-11-18-preserve-unchanged-keyframes-clips-and-cuts
title: Preserve unchanged keyframes, clips and cuts across thumbnail.replaces upgrades
status: done
priority: P2
area: tools
owner: antigravity-heimao-thumbs
claimed_at: 2026-11-18T14:19:26Z
created_at: 2026-11-18T14:19:16Z
completed_at: 2026-11-18T14:19:57Z
branch: claude/thumbnail-replaces-binding
depends_on: []
scope:
  - tools/video/core/schema.mjs
  - tools/video/core/timeline.mjs
  - tools/video/core/timeline.test.mjs
  - tools/video/core/state.mjs
  - tools/video/package/cli.mjs
  - docs/videos/so-thats-why/thumbnails.md
---

# Preserve unchanged keyframes, clips and cuts across thumbnail.replaces upgrades

## Why

When an already-shot or owner-approved episode (`curio-*` or `sothatswhy-*`) upgrades its thumbnail to the full-bleed `layout: "heimao"` / `"heimao-left"` specification introduced in PR #2164 (`74eb4f18`), `visualHash(doc)` moves as intended so `render` redraws `thumbnail.jpg` and all localized `thumbnails/<locale>.jpg`. However, because `pictureHash(doc)` and `checks.json` also bind to `visualHash(doc)`, changing `doc.thumbnail` alone previously marked unchanged `keyframes/manifest.json`, `clips/manifest.json`, and the owner-approved `final.mp4` (`checks.json`) stale even though `final.mp4` never draws `doc.thumbnail`.

## Definition of done

- [x] `video.json` accepts an optional `thumbnail.replaces` (`{ template, data, variants? }`) naming the previous thumbnail configuration.
- [x] `visualHash(doc)` hashes the active thumbnail without `replaces` so `frames/manifest.json` (`frames rendered`) still goes stale and requires a full `render` (`thumbnail.jpg` + `thumbnails/<locale>.jpg`).
- [x] `picturesBound(recorded, doc)` and `cutVisualBound(recorded, doc)` verify unchanged `keyframes/manifest.json`, `clips/manifest.json`, and `checks.json` (`video assembled` and `package`) against `doc.scenes` and `doc.theme` across `thumbnail.replaces`, while any edit to `doc.scenes` or `doc.theme` still invalidates them.
- [x] `docs/videos/so-thats-why/thumbnails.md` documents the `thumbnail.replaces` + `thumbnail.data.asset` upgrade workflow, and unit tests pass.

## Steps

- [x] Validate optional `thumbnail.replaces` in `tools/video/core/schema.mjs`.
- [x] Update `visualHash`, `picturesBound`, and `cutVisualBound` in `tools/video/core/timeline.mjs`, and wire `cutVisualBound` into `tools/video/core/state.mjs` and `tools/video/package/cli.mjs`.
- [x] Add regression unit test in `tools/video/core/timeline.test.mjs` and document the workflow in `docs/videos/so-thats-why/thumbnails.md`.
- [x] Verify `npm run test:tools`, `npm run test:docs-videos`, and `npm run check:tasks`.

## How to verify

```bash
node --test tools/video/core/timeline.test.mjs tools/video/package/package.test.mjs tools/video/core/state.test.mjs
npm run test:docs-videos && npm run check:tasks
```

## Notes

- Claimed with `--force` because two stale October tickets (`2026-10-04-drama-montage-beats-flash-cuts` and `2026-10-27-1-3-5-5-5`, 22–45 days old with zero active branches or open PRs) still list `timeline.mjs` / `schema.mjs` in their scope.
- `MAX_REPLACED_THUMBNAILS` caps `thumbnail.replaces` chain traversal at 4 steps so malformed or deeply nested history fails closed.
