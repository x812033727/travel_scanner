---
id: 2026-09-23-supply-chain-pins-and-announcers
title: Supply chain: base images by digest, uv pin, mailpit latest, red-main fork filter, audit announcer
status: done
priority: P3
area: ops
owner: claude-opus-5-5-supply-chain
claimed_at: 2026-10-02T17:38:09Z
created_at: 2026-09-23T15:57:51Z
completed_at: 2026-10-02T18:08:05Z
branch: claude/supply-chain-pins
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
  - .github/workflows/airline-crawler-validation.yml
  - .github/workflows/article-localization.yml
  - .github/workflows/live-provider-validation.yml
  - .github/workflows/naver-maps-smoke.yml
  - .github/dependabot.yml
  - tools/supply-chain.test.mjs
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

- [x] Every base image in the Dockerfiles, `docker-compose.community.yml` and the workflows
      is pinned `tag@sha256:...` with a `# tag` comment, and `.github/dependabot.yml` has a
      `docker` ecosystem entry so the digests move by pull request.
- [x] `uv` is installed at a pinned version in the API image.
- [x] `ci-red-main.yml` announces only when `github.event.workflow_run.event == 'push'`.
- [x] A failed audit run opens or comments on an issue the same way red main does.

## Steps

- [x] Pin the images (`docker buildx imagetools inspect <image>:<tag>` gives the multi-arch
      digest).
- [x] Add the Dependabot `docker` entries for `/apps/api`, `/apps/web` and `/`.
- [x] Add the `event == 'push'` condition.
- [x] Either extend `ci-red-main.yml` to `workflows: [CI, "npm audit", "pip audit"]` with a
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

### 2026-10-03, claude-opus-5-5-supply-chain (PR on `claude/supply-chain-pins`)

- **Digests** were read without docker (none on this machine): the registry API over HTTPS,
  anonymous pull token, `HEAD /v2/<repo>/manifests/<tag>` with the OCI index Accept header,
  so each is the multi-arch index digest `imagetools inspect` reports. Each was cross-checked
  against Docker Hub's tag API (same value). Pinned, tag unchanged:
  `python:3.13-slim@sha256:bb298871…`, `node:22-alpine@sha256:0a7108bf…`,
  `postgres:17-alpine@sha256:b0f9560a…`, `redis:7.4-alpine@sha256:858f009f…`,
  `nginx:1.28-alpine@sha256:a8b39bd9…`. Mailpit: `latest` was the same digest as `v1.31.3`
  (`ed9b00c6…`), so it is `axllent/mailpit:v1.31.3@sha256:…` — no version change.
- **The tag lives in the reference, not a `# tag` comment** (`python:3.13-slim@sha256:…`).
  Dependabot rewrites the tag and digest of that form together; a comment is the one part it
  would not touch, and it would also break the `*_IMAGE` scan in `tools/ci-images.test.mjs`
  (its regex wants the value alone on the line).
- **Scope grew by the four other workflows with service images** (airline-crawler-validation,
  article-localization, live-provider-validation, naver-maps-smoke): the definition of done
  says "the workflows", and leaving them on bare tags would split `postgres`/`redis` two ways.
  Only their `image:` lines changed. Also `tools/supply-chain.test.mjs`, the guard below.
- **Dependabot cannot see workflow images.** Checked in dependabot-core: `github-actions`
  updates `uses:` only; `docker` reads Dockerfile `FROM` lines and YAML that looks like a
  Kubernetes resource (`apiVersion` + `kind`); `docker-compose` reads `services.*.image` of
  `*compose*.yml` files. So: `docker` for `/apps/api` and `/apps/web`, `docker-compose` for
  `/` (a `docker` entry for `/` would find no Dockerfile and fail), and the workflow images
  are bumped by hand. `tools/supply-chain.test.mjs` fails while one image is pinned two ways,
  so a Dependabot bump of mailpit in the compose file goes red until MAILPIT_IMAGE follows.
- **Dependabot ignores minor and major tags** for all three docker entries, so it only moves
  digests and patch tags: Python 3.14 is a "minor" bump to Dependabot but needs uv.lock's
  `requires-python`, Node 24 and PostgreSQL 18 are migrations. The root compose entry also
  sees `docker-compose.yml` / `docker-compose.prod.yml`; their bare tags get no pull request.
- **uv** is `uv==0.12.22`, what the last main CI run's setup-uv and the image build both
  installed (2026-10-02; nothing in the repository pinned it). Dependabot does not read a
  pip pin inside `RUN`, so it is bumped by hand; the containers job builds the image, so a
  lock this uv cannot read fails CI first.
- **Red main**: `workflows: [CI, "npm audit", "pip audit"]`, one label (and so one open issue)
  per workflow: `ci-red-main`, `npm-audit-red`, `pip-audit-red`; `issues.create` makes a
  missing label (that is how `ci-red-main` got its #ededed). The `if:` requires
  `workflow_run.event` to be `push` or `schedule`. Verified against real runs
  (`gh api .../actions/workflows/<file>/runs`): main's CI is `push`, every pull request run
  is `pull_request` (a fork can start nothing else here: no `pull_request_target`), and both
  audits are `schedule` on head branch `main`. `workflow_dispatch` audit runs are not
  announced; whoever started one is watching it. Recent audit runs on main did fail
  (npm audit twice, pip audit once), which nobody was told about until now.
- **Not pinned:** `quay.io/minio/minio` and `quay.io/minio/mc` in the community compose file.
  quay.io answers an anonymous manifest request with 401, so there is no digest to read, and
  `2026-09-24-run-the-local-community-storage-without` replaces them (and pins by digest).
  The test lists them as exceptions tied to that task and fails once the task is closed.
- **Filed** `2026-10-02-pin-remaining-base-images-by-digest` for `docker-compose.yml`,
  `docker-compose.prod.yml`, `ops/video/Dockerfile` and `ops/youtube-uploader/Dockerfile`.
- Workflows cannot run locally: YAML parsed with js-yaml, the github-script body run against
  fake `github`/`context` objects for all three workflow names plus an unknown one. The
  announcer itself only runs on main after merge; the pinned service images and
  `*_IMAGE` values prove themselves on the pull request's own CI run.
