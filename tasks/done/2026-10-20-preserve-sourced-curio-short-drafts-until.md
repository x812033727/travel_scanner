---
id: 2026-10-20-preserve-sourced-curio-short-drafts-until
title: Preserve sourced Curio Short drafts until episode claims clear
status: done
priority: P2
area: docs
owner: codex-root
claimed_at: 2026-10-20T05:41:27Z
created_at: 2026-10-20T05:41:24Z
completed_at: 2026-10-20T05:42:16Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/shorts-drafts
---

# Preserve sourced Curio Short drafts until episode claims clear

## Why

Five completed Curio long episodes need the series-required single Short, but their episode directories are held by under-24-hour in-progress tasks that are not active in this thread. Independent scripts in `/tmp` would be lost when this workspace is replaced. Preserve them under a distinct scope without modifying the claimed episode directories.

## Definition of done

- [x] S02/S03/S04/S23/S30 source-safe one-Short JSON drafts are reviewable in a neutral directory, with exact hashes and handoff instructions.
- [x] Existing task claims and episode directories remain untouched.
- [x] Each copy passes the one-Curio schema and selected-keyframe hash check; unbuilt and unlinked gates are explicit.

## Steps

- [x] Copy the independently reviewed `/tmp` scripts after checking their exact SHA-256 values.
- [x] Validate the copies against each episode's selected `keyframes/manifest.json` and document the limits.

## How to verify

`node --input-type=module` importing `episodeShortsProblems`, `episodeShort` and `verifyEvidence` for all five copied JSON scripts (2026-10-20: S02 6, S03 6, S04 7, S23 6, S30 6 bound assets); `sha256sum docs/videos/shorts-drafts/*.json`; `npm run check:tasks`.

## Notes

These are portable drafts, not episode-owned `shorts.json`, Shorts media, site reviews or upload packages. In particular, none has a verified 25–55-second duration or full-video YouTube URL. The next producer must claim the episode scope before moving a draft there.
