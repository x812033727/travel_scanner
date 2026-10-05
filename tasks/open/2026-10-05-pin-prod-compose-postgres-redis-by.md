---
id: 2026-10-05-pin-prod-compose-postgres-redis-by
title: Pin the production compose postgres and redis images by digest
status: open
priority: P3
area: ops
owner:
claimed_at:
created_at: 2026-10-05T01:37:36Z
completed_at:
branch:
depends_on: []
scope:
  - docker-compose.prod.yml
  - tools/supply-chain.test.mjs
  - .github/dependabot.yml
---

# Pin the production compose postgres and redis images by digest

## Why

`docker-compose.prod.yml` still runs `postgres:17-alpine` and `redis:7.4-alpine`, tags their
publisher can move. Every other image in the repository is pinned `tag@sha256:digest`
(the API, web, video worker and uploader Dockerfiles, `docker-compose.yml`,
`docker-compose.community.yml` and the workflows), and `tools/supply-chain.test.mjs` keeps
them that way. So the production database and queue are the two images that can change
under a deploy with no diff in this repository.

This was split from `2026-10-02-pin-remaining-base-images-by-digest`, which pinned the rest.
It is separate because it is the only part that needs the production host: changing a
service's `image:` makes compose recreate that container on the next deploy, so the
production postgres and redis restart, and if the host's local `postgres:17-alpine` is older
than the pinned digest the restart also moves PostgreSQL to a newer 17.x patch.

## Definition of done

- [ ] `postgres` and `redis` in `docker-compose.prod.yml` use the same `tag@sha256:digest`
      reference as `docker-compose.yml` and the workflows (or a newer digest copied into all
      of them in the same change).
- [ ] `tools/supply-chain.test.mjs` scans `docker-compose.prod.yml`: it is in `COMPOSE_FILES`
      and no longer in `COMPOSE_NOT_SCANNED_YET`, and the locally built
      `travel-scanner-*:${RELEASE_SHA:-local}` images are skipped by an explicit rule, not by
      loosening the digest check.
- [ ] The comment above the `docker-compose` entry in `.github/dependabot.yml` no longer says
      the production compose file is unpinned.
- [ ] The deploy that carries the pin restarted postgres and redis cleanly: both healthy in
      `docker compose ps`, `/ready` answers, and the PostgreSQL version is the one expected.

## Steps

- [ ] On the host, before the deploy, record what runs now:
      `docker image inspect postgres:17-alpine --format '{{json .RepoDigests}}'`, the same for
      `redis:7.4-alpine`, and `SELECT version();` in the database. If the digest differs from
      the pin, the deploy also upgrades the patch version; say so in the PR.
- [ ] Pin both images, extend the test, update the Dependabot comment.
- [ ] Deploy through the `deploy` skill at a time a short database and queue restart is
      acceptable; a staged release must follow `ops/release/README.md`.

## How to verify

```bash
node --test tools/supply-chain.test.mjs
npm run test:tools
docker compose -f docker-compose.prod.yml config --quiet
```

On the host after the deploy: `docker compose -f docker-compose.prod.yml ps` shows `postgres`
and `redis` healthy on the pinned image, and the site's `/ready` is OK.

## Notes

- Split from `2026-10-02-pin-remaining-base-images-by-digest`. On 2026-10-05 the tags still
  resolved to the digests the workflows pin: `postgres:17-alpine@sha256:b0f9560a2de083e2cc7382e75f808c7381a32852a7ec49117deedb300e552b24`
  and `redis:7.4-alpine@sha256:858f009f9709ce576febc734aa78b8f6d624b82571f9ddb6bda4377c833b3499`
  (both OCI indexes, multi-arch). Re-read them before pinning; the method is in that task's
  Notes.
- `docker-compose.prod.yml` is also the whole scope of
  `2026-09-13-prod-compose-network-segmentation` (blocked). This can be done inside that task;
  if it is done on its own, check that task is not in progress first.
- The test's `image:` scan reads every `image:` line, so the `travel-scanner-api`,
  `travel-scanner-web` and `travel-scanner-video-worker` images (built on the host, tagged with
  the release SHA) will show up as unpinned until they are skipped.
- Dependabot's root `docker-compose` entry already reads this file; once it is pinned, its
  digest pull requests cover it too, and the supply-chain test keeps the three references
  equal.
