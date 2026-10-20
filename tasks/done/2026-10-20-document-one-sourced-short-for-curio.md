---
id: 2026-10-20-document-one-sourced-short-for-curio
title: Document one sourced Short for Curio episodes
status: done
priority: P2
area: docs
owner: codex-root
claimed_at: 2026-10-20T05:36:20Z
created_at: 2026-10-20T05:36:17Z
completed_at: 2026-10-20T05:37:04Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - .agents/skills/youtube-video/references/shorts.md
  - docs/videos/SHORTS.md
---

# Document one sourced Short for Curio episodes

## Why

`history-curiosity/README.md` requires one Short per `curio-*` episode. The shared Shorts reference and design still say every sourced episode has two, which could lead the next producer to draft an extra Short.

## Definition of done

- [x] The Shorts skill and design state that Curio uses one sourced Short and other episode lines use two.
- [x] The existing rule that Shorts need the long video's real YouTube URL for metadata and links remains explicit.

## Steps

- [x] Update the existing skill reference and design wording.
- [x] Check the Curio validator focused tests and S34 `from-episode --check` in the producer's companion task.

## How to verify

`rg -n '奇聞檔案局|curio-' .agents/skills/youtube-video/references/shorts.md docs/videos/SHORTS.md`; companion task runs `node --test tools/video/shorts/episode.test.mjs` and S34 `from-episode --check`.

## Notes

Only `.agents/skills/youtube-video/references/shorts.md` exists; the `.claude` skill mirror contains `SKILL.md` alone, so no reference file was created there. Source link and package gates remain real until the corresponding long video has a YouTube ID.
