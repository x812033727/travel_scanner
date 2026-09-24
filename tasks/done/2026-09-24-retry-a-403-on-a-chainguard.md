---
id: 2026-09-24-retry-a-403-on-a-chainguard
title: Retry a 403 on a Chainguard blob or config download in pull-images.sh
status: done
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-24T16:24:48Z
created_at: 2026-09-24T16:24:38Z
completed_at: 2026-09-24T16:30:07Z
branch: claude/ci-pull-retry-cgr-403
depends_on: []
scope:
  - tools/ci/pull-images.sh
  - tools/ci-images.test.mjs
---

# Retry a 403 on a Chainguard blob or config download in pull-images.sh

## Why

At 15:39:43Z on 2026-09-24 the `api` job of run 36021704422 (PR #736, job 107708075876)
failed in its first step. `tools/ci/pull-images.sh` stopped at once after docker printed:

```
error pulling image configuration: download failed after attempts=1: denied: <!doctype html><meta charset="utf-8"><meta name=viewport content="width=device-width, initial-scale=1"><title>403</title>403 Forbidden
```

The script reads any `denied` as a refusal and does not retry it. dockerd, though, prints
**any** HTTP 403 as `denied: <body>`, including a 403 on a blob after the registry has
already served the manifest. This one was not a refusal:

- The same digest pulled successfully in seven other jobs between 15:37:26 and 15:40:21:
  run 36021461417 (main, api and full-stack-smoke), 36021621851 (PR #735, both jobs) and
  36021701956 (PR #733, both jobs). One of the seven was the `full-stack-smoke` job of the
  **same run**, 38 seconds later, and it ran in the same Azure region (westus3). The job's
  rerun pulled it at 15:56:08Z.
- Docker had got as far as the config blob, so the token and the manifest had both been
  served.
- The body is HTML from cgr.dev's front end (`server: Google Frontend`). Blobs are served by
  a 307 to a presigned Cloudflare R2 URL, and R2 answers errors in XML. So the 403 most likely
  came from an edge rule in front of the registry, not from the image or its permissions.

A 403 on a blob or config download should get the same retries as a 502. A 401
(`unauthorized`, which is how quay.io answered in #734) and a denial on the manifest or token
are still refusals.

## Definition of done

- [x] A 403 on a blob or config download is retried with the usual backoff, in both dockerd's
      wording (`error pulling image configuration` / `download failed after attempts`
      … `denied:`) and the containerd image store's (`…/blobs/sha256:…: 403 Forbidden`).
- [x] A 401 on the manifest (the quay.io case) or on a blob, and a `denied` on the manifest
      (the Docker Hub case), still fail at once.
- [x] If every attempt gets a blob 403, the final error says what that means, so a permanent
      change on the registry's side is not read as a flake.
- [x] The two open questions are answered with evidence: is `docker login` needed, and does a
      pinned digest age out?

## Steps

- [x] Classify a blob/config 403 before the refusal check in `tools/ci/pull-images.sh`, with
      its own warning, and explain it in the script's header.
- [x] Tests in `tools/ci-images.test.mjs` with the literal CI message, the containerd form,
      the quay.io 401 and a blob 401. The three new 403 tests fail against the old script.
- [x] Probe cgr.dev anonymously for the pinned digest, `:latest` and older digests.

## How to verify

```bash
node --test tools/ci-images.test.mjs
```

The new cases are "retries a 403 on a blob or config download", "gives up on a blob 403 that
every attempt gets" and "does not retry a 401". To see the old behaviour fail them, run them
against `git show origin/main:tools/ci/pull-images.sh`.

## Notes

**Is `docker login` necessary? No.** On 2026-09-24 at 16:20Z,
`https://cgr.dev/token?scope=repository:chainguard/minio:pull` issued an anonymous token.
With that token, the index, the amd64 manifest, the config and every layer blob all came back
200/206. All eight CI pulls around the failure were anonymous, and seven of them succeeded.
Chainguard documents anonymous tokens for its free tier. A login would need a Chainguard
account and an Actions secret. Dependabot pull requests do not get Actions secrets, so they
would still pull anonymously. Nothing shows that the 403 was an anonymous-only limit.

**Did a pinned digest age out? No, and on current evidence it will not.**

- When the job failed, the pinned digest `sha256:bd014394…` *was* `:latest`. The index was
  created at 2026-09-24T02:26:45Z, and `HEAD /v2/chainguard/minio/manifests/latest` still
  returned that digest at 16:20Z.
- Chainguard's policy (June 2023, "A guide on how to use Chainguard Images for public catalog
  tier users") says: "All users across all tiers will continue to have access to pulling by
  digest." Only *tags* other than `:latest` and `:latest-dev` were withdrawn from the free
  tier.
- The repository keeps cosign `.sig`/`.att` tags for 1,269 older digests (indexes and
  per-platform manifests). I sampled 16 of them,
  built between 2025-11-12 and 2026-09-16. All 16 still served their manifest and config
  anonymously (307 to R2, then 200). The oldest (`be7b002d2d49…`, 2025-11-12) served all 11
  layers.
- Another project's issue (enorm-labs/event-junkie#1859) assumed that old digests stop being
  pullable. It cites no failure that shows this.

**If that ever changes**, the symptoms will differ. A manifest that has gone away answers
`manifest unknown` or a 401/403 on the manifest; the script refuses those at once. A registry
that serves the manifest but 403s the blobs every time runs through the retries and ends with
the "stopped serving this image's content anonymously" error. The options, cheapest first:

1. Bump the pin to the current `:latest` (the recipe is in the Notes of
   `tasks/done/2026-09-24-pull-minio-for-ci-from-a.md`). This keeps CI reproducible.
2. Resolve `:latest` at run time and log its digest. It never ages out, but a new MinIO build
   could then change CI underneath a pull request that did not touch it. Also,
   `tools/ci-images.test.mjs`'s single-image-per-variable check would need to accept a tag
   again. Use this only as a fallback that logs a `::warning::` when the pin fails.
3. Mirror the pinned digest into GHCR with `docker buildx imagetools create` (same digest,
   both platforms). Pull it with `GITHUB_TOKEN`, keeping the package private: MinIO is AGPL,
   and a public copy would be redistribution. This removes cgr.dev from CI entirely, including
   its transient 403s.
4. Cache `docker save` of the pinned digest with `actions/cache`, keyed on the digest, and
   fall back to the pull on a miss.
5. Log in to cgr.dev with a Chainguard pull token. Only worth it if blob 403s turn out to be an
   anonymous limit, and Dependabot PRs still would not have the secret.

Also: Chainguard has removed images from its free tier before (2024-11-21). If MinIO is
removed, the pull fails as a manifest refusal, not as a 403 on a blob. Options 1 and 2 stop
working, and 5 needs a paid catalog. Only a copy made beforehand (3, or 4 while the cache
holds) keeps CI running.
