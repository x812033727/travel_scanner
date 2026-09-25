---
id: 2026-09-25-the-video-worker-s-docs-volume
title: The video worker's docs volume never takes files from a newer image
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-25T12:50:29Z
completed_at:
branch:
depends_on: []
scope:
  - ops/video
---

# The video worker's docs volume never takes files from a newer image

## Why

`ops/video/Dockerfile` copies `docs/videos` into the image. `docker-compose.prod.yml` then
mounts the named volume `video_docs` over the same path. Docker fills a named volume from the
image only once, when the volume is created. The volume was created on 2026-09-25, and every
later deploy leaves it as it was. On the host it holds `AUTOMATION.md`, `DESIGN.md` and
`README.md` from that first deploy, plus the worker's own drafts.

Nothing reads those three files at run time today, so nothing is broken yet. It will break when:

- a video or a shared file is merged into `docs/videos` on main (for example the pilot, batch 2,
  or `lexicon.json`), and the worker is expected to see it; or
- a file in there changes on main and the worker is expected to use the new version.

## Definition of done

- [ ] After a deploy, files from the image that the worker does not own are up to date in
      the worker's `docs/videos`. Video folders the worker made are never overwritten.
- [ ] A decision on `lexicon.json` is written down: either the worker owns it (it merges
      terms into it today), or the repository's copy is merged into the worker's.

## Steps

- [ ] Keep the image's copy at a second path (for example `/opt/mokaair/docs-seed/videos`).
      `worker.sh` then syncs it into the volume on start: top-level files are replaced, and a
      video folder is copied only when the volume does not already have it.
- [ ] Test it with a smoke-stage check in the Dockerfile.

## How to verify

Change `docs/videos/README.md` on a branch, build the image, and start the worker on an
existing volume. The new README is in the volume and the worker's drafts are untouched.

## Notes

Found while working on `2026-09-25-let-the-owner-drop-a-video`. The first automatic draft
could not see the pilot or batch 2. That ticket fixes it through the site's video list, not
through this volume.
