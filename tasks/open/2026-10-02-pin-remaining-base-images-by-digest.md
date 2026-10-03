---
id: 2026-10-02-pin-remaining-base-images-by-digest
title: Pin the remaining base images by digest: dev and production compose, video worker, uploader
status: open
priority: P3
area: ops
owner:
claimed_at:
created_at: 2026-10-02T17:56:20Z
completed_at:
branch:
depends_on: []
scope:
  - docker-compose.yml
  - docker-compose.prod.yml
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

- [ ] Each image above is pinned `tag@sha256:digest`, with the same reference the workflows
      already use where it is the same image (postgres and redis).
- [ ] `tools/supply-chain.test.mjs` scans these files too, so an unpinned image fails
      `npm run test:tools`.
- [ ] Dependabot moves the new digests: `docker` entries for `/ops/video` and
      `/ops/youtube-uploader` with the same `ignore` as the existing docker entries
      (the root `docker-compose` entry already covers both compose files).

## Steps

- [ ] Read each digest without docker: `node` against the registry API
      (`HEAD /v2/<repo>/manifests/<tag>` with the OCI index Accept header, plus an anonymous
      pull token when the registry answers 401) or `docker buildx imagetools inspect <image:tag>`;
      cross-check Docker Hub's `hub.docker.com/v2/repositories/library/<name>/tags/<tag>` `digest`.
      Both images were readable that way on 2026-10-03.
- [ ] Pin, extend `DOCKERFILES` / `COMPOSE_FILES` in the test, add the Dependabot entries.
- [ ] Production compose: do it after (or inside) `2026-09-13-prod-compose-network-segmentation`,
      whose scope is that file; a pin there takes effect on the next deploy.

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
