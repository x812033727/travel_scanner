---
id: 2026-09-25-the-video-worker-s-docs-volume
title: The video worker's docs volume never takes files from a newer image
status: done
priority: P2
area: ops
owner: codex-gpt6-worker-docs
claimed_at: 2026-09-30T03:09:21Z
created_at: 2026-09-25T12:50:29Z
completed_at: 2026-09-30T03:20:55Z
branch: codex/video-docs-refresh
depends_on: []
scope:
  - ops/video/Dockerfile
  - ops/video/Dockerfile.dockerignore
  - ops/video/worker.sh
  - ops/video/sync-docs.mjs
  - ops/video/sync-docs.test.mjs
  - ops/video/README.md
---

# The video worker's docs volume never takes files from a newer image

## Why

`ops/video/Dockerfile` copies `docs/videos` into the image. `docker-compose.prod.yml` then
mounts the named volume `video_docs` over the same path. Docker fills a named volume from the
image only once, when the volume is created. The volume was created on 2026-09-25, and every
later deploy leaves it as it was. On the host it holds `AUTOMATION.md`, `DESIGN.md` and
`README.md` from that first deploy, plus the worker's own drafts.

The planner now reads README.md at runtime, so stale shared documents can already
affect its behavior. The same problem applies when:

- a video or a shared file is merged into `docs/videos` on main (for example the pilot, batch 2,
  or `lexicon.json`), and the worker is expected to see it; or
- a file in there changes on main and the worker is expected to use the new version.

## Definition of done

- [x] After a deploy, files from the image that the worker does not own are up to date in
      the worker's `docs/videos`. Video folders the worker made are never overwritten.
- [x] A decision on `lexicon.json` is written down: either the worker owns it (it merges
      terms into it today), or the repository's copy is merged into the worker's.

## Steps

- [x] Keep the image's copy at a second path (for example `/opt/mokaair/docs-seed/videos`).
      `worker.sh` then syncs it into the volume on start: top-level files are replaced, and a
      video folder is copied only when the volume does not already have it.
- [x] Test it with a smoke-stage check in the Dockerfile.

## How to verify

Change `docs/videos/README.md` on a branch, build the image, and start the worker on an
existing volume. The new README is in the volume and the worker's drafts are untouched.

## Notes

- 2026-09-30 audit at main 7c8e524d: no overlapping open PR or dirty files in
  177 existing worktrees. The other worker.sh ticket is unclaimed. The old note
  that nothing reads the documents is stale: prompts.mjs now reads README.md.
- Chosen ownership: existing video directories and lexicon.json belong to the
  worker. Seed them only when absent; refresh the other top-level image files
  on startup. No volume pruning, compose changes or production operations.
- Implemented immutable image seed at `/opt/mokaair/docs-seed/videos` and
  startup synchronization before pairing, ticks or model work. Root documents
  are replaced atomically; new folders are staged before installation; initial
  lexicon creation cannot overwrite a concurrent worker dictionary. Copy failures,
  symlinks in copied trees, overlapping roots and incompatible destination types
  stop startup. Existing worker folders are never traversed or filled in.
- Validation: bundled Node 24.19 Windows sync suite 7 passed / 4 platform skips;
  full tools suite 917 passed / 2 platform skips after rebasing onto main
  64f132e1; worker shell syntax and task
  checks passed. Eleven sync tests are wired into the Docker smoke stage as
  nonroot `pwuser`, followed by default-path initialization and media smoke.
  Docker is unavailable locally; the Linux permission/link cases and image
  integration are CI acceptance, not a production deployment claim.
- Independent review verified preservation during concurrent dictionary/folder
  creation, incompatible type rejection and staging cleanup. Final audit found
  no overlap across 18 open PRs, 50 remote heads and 177 accessible worktrees.
- After the rebase, all 17 open PRs still avoid the six ops files. The newly
  merged branding documents follow the root-file policy; branding assets and
  pins live outside the docs volume and remain untouched.
Found while working on `2026-09-25-let-the-owner-drop-a-video`. The first automatic draft
could not see the pilot or batch 2. That ticket fixes it through the site's video list, not
through this volume.
