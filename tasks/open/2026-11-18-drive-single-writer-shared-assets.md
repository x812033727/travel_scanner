---
id: 2026-11-18-drive-single-writer-shared-assets
title: One writer per Drive file: sessions stop copying the final cut, shared assets folder
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-18T02:27:51Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/ai-drama-drive
  - docs/videos/AI-DRAMA-DRIVE.md
  - tools/video/import/series-backup.mjs
---

# One writer per Drive file: sessions stop copying the final cut, shared assets folder

## Why

An episode's final cut, clips and recordings are on Drive twice: once from the host worker's upload package, once inside 製作檔/ from the session's todrive.sh. Music libraries are duplicated per series, and four near-identical upload tools exist (todrive.sh, tn-drive.py, series-backup.mjs, migrate.py).

## Definition of done

- [ ] The worker is the only writer of an episode's package; todrive.sh excludes what the worker copies.
- [ ] One `AI/共用素材/` for music, character sheets and references, linked from each series.
- [ ] One upload tool.

## Steps

- [ ] Decide the exclude list with the owner (lessons/shared.md §十三 warns against skipping folders).
- [ ] Move shared libraries once, with a manifest, leaving the old copies in _舊版.

## How to verify

See the steps; each lands with tests.

## Notes

Phase 3 of the Drive plan.
