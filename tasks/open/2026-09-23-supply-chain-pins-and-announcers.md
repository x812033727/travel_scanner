---
id: 2026-09-23-supply-chain-pins-and-announcers
title: Supply chain: base images by digest, uv pin, mailpit latest, red-main fork filter, audit announcer
status: open
priority: P3
area: ops
owner:
claimed_at:
created_at: 2026-09-23T15:57:51Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/Dockerfile
  - apps/web/Dockerfile
  - docker-compose.community.yml
  - .github/workflows/ci-red-main.yml
  - .github/workflows/npm-audit.yml
  - .github/workflows/pip-audit.yml
  - .github/workflows/ci.yml
  - .github/workflows/travel-discovery.yml
  - .github/dependabot.yml
---

# Supply chain: base images by digest, uv pin, mailpit latest, red-main fork filter, audit announcer

## Why

Everything that runs in CI is pinned by SHA and refreshed by Dependabot since 2026-09-14, but
the images the product runs on are not: `python:3.13-slim`, `node:22-alpine`,
`postgres:17-alpine`, `redis:7.4-alpine`, `nginx:1.28-alpine` are mutable tags,
`pip install --no-cache-dir uv` in the API image takes whatever uv is current, and
`axllent/mailpit:latest` is used by the community compose and two workflows. A registry-side
tag move changes the production image on the next `--build` with no diff in the repository.

Two smaller CI items. `ci-red-main.yml` triggers on `workflow_run` with `branches: [main]`,
which filters on the triggering run's head branch name, so a fork pull request whose branch
is literally `main` and fails CI files a "CI is red on main" issue (body fields are
GitHub-generated, so no injection, just a false alarm). And the daily `npm-audit.yml` /
`pip-audit.yml` fail their own run on a known advisory but nothing announces it, so only the
last committer's email notices.

## Definition of done

- [ ] Every base image in the Dockerfiles, `docker-compose.community.yml` and the workflows
      is pinned `tag@sha256:...` with a `# tag` comment, and `.github/dependabot.yml` has a
      `docker` ecosystem entry so the digests move by pull request.
- [ ] `uv` is installed at a pinned version in the API image.
- [ ] `ci-red-main.yml` announces only when `github.event.workflow_run.event == 'push'`.
- [ ] A failed audit run opens or comments on an issue the same way red main does.

## Steps

- [ ] Pin the images (`docker buildx imagetools inspect <image>:<tag>` gives the multi-arch
      digest).
- [ ] Add the Dependabot `docker` entries for `/apps/api`, `/apps/web` and `/`.
- [ ] Add the `event == 'push'` condition.
- [ ] Either extend `ci-red-main.yml` to `workflows: [CI, "npm audit", "pip audit"]` with a
      label per workflow, or add a small announcer workflow.

## How to verify

```bash
npm run test:tools
docker compose -f docker-compose.community.yml config --quiet
```

## Notes

- Found in the 2026-09-23 security review (findings L10, L11, I4).
- `docker-compose.prod.yml` also carries the postgres/redis tags but is held by
  `2026-09-13-prod-compose-network-segmentation`; pin those there or after it lands.
