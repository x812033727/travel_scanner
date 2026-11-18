---
id: 2026-11-18-drive-single-writer-shared-assets
title: One writer per Drive file: sessions stop copying the final cut, shared assets folder
status: review
priority: P2
area: tools
owner: claude-opus-5-5-drive-single-writer
claimed_at: 2026-11-18T05:42:53Z
created_at: 2026-11-18T02:27:51Z
completed_at:
branch: claude/kind-mccarthy-5m28jo
depends_on: []
scope:
  - docs/videos/ai-drama-drive/todrive.sh
  - docs/videos/ai-drama-drive/todrive-plan.mjs
  - docs/videos/ai-drama-drive/todrive.test.mjs
  - docs/videos/AI-DRAMA-DRIVE.md
  - docs/videos/explainer-series/music-library/README.md
---

# One writer per Drive file: sessions stop copying the final cut, shared assets folder

## Why

An episode's final cut, clips and recordings are on Drive twice: once from the host worker's upload package, once inside 製作檔/ from the session's todrive.sh. Music libraries are duplicated per series, and four near-identical upload tools exist (todrive.sh, tn-drive.py, series-backup.mjs, migrate.py).

## Definition of done

- [x] A file the worker already holds with the same bytes is not uploaded twice; todrive.sh records where the worker's copy is (owner's choice over "the worker is the only writer").
- [x] One `AI劇/_共用素材/<種類>/<名稱>/` for new shared assets; existing per-series libraries stay (owner's choice).
- [x] One upload tool: todrive.sh (tn-drive.py only wraps it; migrate.py was a one-off).
- [x] Each 製作檔 upload leaves a manifest.json + SHA256SUMS (moved here from the index task).

## Steps

- [x] Decide the exclude list with the owner: only secrets and node_modules/.venv, each recorded in the manifest; worker-held identical files are listed, not re-uploaded.
- [x] ~~Move shared libraries once~~: the owner chose not to move existing libraries (2026-11-18).

## How to verify

See the steps; each lands with tests.

## Notes

Phase 3 of the Drive plan.

Owner, 2026-11-18: keep "everything"; skip only a file the worker already holds with the same bytes
(both backup.json's sha256 and the folder's size and md5 must agree), and put new shared assets in
`AI劇/_共用素材/<種類>/<名稱>/` without moving the existing ones.

Done on branch claude/kind-mccarthy-5m28jo: todrive-plan.mjs (plan, exclusions, worker match),
todrive.sh (files-from upload, check, `_todrive/<time>/manifest.json` + SHA256SUMS + latest.json,
--check re-verifies worker copies), todrive.test.mjs with a fake rclone, AI-DRAMA-DRIVE.md §清單與不重複
and §共用素材, music-library README.

Left for a follow-up, because other in-progress tasks claim those files:
- `.agents/skills/curio-episode/SKILL.md` (and its `.claude` copy) gives the destination as
  `AI劇/奇聞檔案局/<代碼>/製作檔/`, missing the `<分類>/` level, and should mention the manifest.
- `docs/videos/BACKUP.md` §資料夾排法 should show `AI劇/_共用素材/` and `_todrive/`.
- `tools/video/import/series-backup.mjs`'s header still names the old `AI/備份/drama/.../_series` path.
