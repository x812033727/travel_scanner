---
id: 2026-10-02-pin-remaining-base-images-by-digest
title: Pin the remaining base images by digest: dev and production compose, video worker, uploader
status: done
priority: P3
area: ops
owner: claude-opus-5-5-pin-base-images
claimed_at: 2026-10-05T01:34:21Z
created_at: 2026-10-02T17:56:20Z
completed_at: 2026-10-05T02:13:57Z
branch: claude/pin-base-images
depends_on: []
scope:
  - docker-compose.yml
  - ops/video/Dockerfile
  - ops/youtube-uploader/Dockerfile
  - .github/dependabot.yml
  - tools/supply-chain.test.mjs
---

# Pin the remaining base images by digest: dev and production compose, video worker, uploader

## Why

`2026-09-23-supply-chain-pins-and-announcers` pinned the API and web Dockerfiles, the
community compose file and every workflow image as `tag@sha256:digest`, and
`tools/supply-chain.test.mjs` keeps them that way. Four files were outside its scope and
still run mutable tags, so a tag moved on the registry changes what they run with no diff
in the repository:

- `docker-compose.prod.yml`: `postgres:17-alpine`, `redis:7.4-alpine` — the production
  database and queue. This file was held by `2026-09-13-prod-compose-network-segmentation`.
- `docker-compose.yml`: the same two tags for local development.
- `ops/video/Dockerfile`: `mcr.microsoft.com/playwright:v1.63.0-noble` (the video worker).
- `ops/youtube-uploader/Dockerfile`: `node:24-bookworm-slim`.

## Definition of done

- [x] `docker-compose.yml`, `ops/video/Dockerfile` and `ops/youtube-uploader/Dockerfile` are
      pinned `tag@sha256:digest`, with the same reference the workflows already use where it is
      the same image (postgres and redis).
- [ ] `docker-compose.prod.yml` pinned the same way — split to
      `2026-10-05-pin-prod-compose-postgres-redis-by` (see Notes).
- [x] `tools/supply-chain.test.mjs` scans these three files too, so an unpinned image fails
      `npm run test:tools`; `docker-compose.prod.yml` is listed as not scanned yet under the
      follow-up's id, and the test fails once that task closes without scanning it.
- [x] Dependabot moves the new digests: `docker` entries for `/ops/video` and
      `/ops/youtube-uploader` with the same `ignore` as the existing docker entries
      (the root `docker-compose` entry already covers both compose files).

## Steps

- [x] Read each digest without docker: `node` against the registry API
      (`HEAD /v2/<repo>/manifests/<tag>` with the OCI index Accept header, plus an anonymous
      pull token when the registry answers 401) or `docker buildx imagetools inspect <image:tag>`;
      cross-check Docker Hub's `hub.docker.com/v2/repositories/library/<name>/tags/<tag>` `digest`.
      Both images were readable that way on 2026-10-03.
- [x] Pin, extend `DOCKERFILES` / `COMPOSE_FILES` in the test, add the Dependabot entries.
- [ ] Production compose: do it after (or inside) `2026-09-13-prod-compose-network-segmentation`,
      whose scope is that file; a pin there takes effect on the next deploy. Split to
      `2026-10-05-pin-prod-compose-postgres-redis-by`.

## How to verify

```bash
node --test tools/supply-chain.test.mjs
npm run test:tools
```

## Notes

- Dependabot's `docker` ecosystem reads `FROM` lines (not `COPY --from`) and Kubernetes
  manifests; `docker-compose` reads `services.*.image` of every `docker-compose*.yml` /
  `compose*.yml` in its directory. Nothing reads the images in `.github/workflows`.
- `postgres:17-alpine` → `18-alpine` is a dump-and-restore migration, which is why the
  Dependabot entries ignore minor and major tags and only move digests and patch tags.
- 2026-10-05 (claude-opus-5-5-pin-base-images): digests read anonymously with `node` `fetch`
  (HEAD and GET `/v2/<repo>/manifests/<tag>` with the OCI index and manifest-list Accept
  headers; a pull token from `auth.docker.io` for Docker Hub, none needed for MCR). For every
  image the HEAD `Docker-Content-Digest`, the SHA-256 of the GET body and (Docker Hub) the Hub
  tags API `digest` agreed, and each is an OCI image index, so the pin stays multi-arch:
  - `node:24-bookworm-slim@sha256:0e0ff40c…f9b6` (linux/amd64, arm64/v8, ppc64le)
  - `mcr.microsoft.com/playwright:v1.63.0-noble@sha256:eff16c30…4a27` (linux/amd64, arm64)
  - `postgres:17-alpine` and `redis:7.4-alpine` still resolve to the digests the workflows
    already pin (`b0f9560a…2b24`, `858f009f…3499`), so `docker-compose.yml` copies those
    references unchanged.
- `node` now runs as two tags on purpose (the web image on `22-alpine`, the uploader on
  `24-bookworm-slim`, which `playwright install --with-deps` needs), and the "one image is
  pinned the same way everywhere" test compared by name only, so it failed as soon as the
  uploader was scanned. `SEVERAL_TAGS` in the test lets a listed name run more than one tag;
  each tag still has to carry one digest everywhere, and the test fails if the name drops back
  to one tag.
- A new test lists every `docker-compose*.yml` / `compose*.yml` at the root (what Dependabot's
  `docker-compose` entry reads) and fails on one that is neither in `COMPOSE_FILES` nor in
  `COMPOSE_NOT_SCANNED_YET` with an open task.
- The Playwright tag has to move with `@playwright/test` (`package-lock.json`,
  `ops/video/package.json`): the image carries that version's browsers. The Dependabot comment
  says so; a digest-only bump does not change the version.
- Both images are built by CI when their directory changes (`video-worker-image.yml`,
  `youtube-uploader.yml`), which is what proves the pinned digests pull and build; there is no
  docker on the machine this was done on. That the two new Dependabot entries parse shows only
  after merge (Insights → Dependency graph → Dependabot).
- Split: `docker-compose.prod.yml` was dropped from this task's scope and moved, with its
  unticked items, to `2026-10-05-pin-prod-compose-postgres-redis-by`. Changing its image
  reference recreates the production postgres and redis containers on the next deploy, and
  should be checked against the digest the host runs now, which needs the host.
