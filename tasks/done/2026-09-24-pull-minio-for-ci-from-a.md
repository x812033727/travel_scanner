---
id: 2026-09-24-pull-minio-for-ci-from-a
title: Pull MinIO for CI from a registry that still serves it anonymously
status: done
priority: P1
area: tools
owner: claude-opus-5-5
claimed_at: 2026-09-24T15:11:03Z
created_at: 2026-09-24T15:11:02Z
completed_at: 2026-09-24T15:12:29Z
branch: claude/ci-minio-chainguard
depends_on: []
scope:
  - .github/workflows/ci.yml
  - tools/ci/pull-images.sh
---

# Pull MinIO for CI from a registry that still serves it anonymously

## Why

On 2026-09-24, between 12:25 and 15:04 UTC, MinIO made `quay.io/minio/minio` and
`quay.io/minio/mc` require a login: the repository API answers 401, and an anonymous pull
token gets 401 on the manifest, while other public quay.io repositories still answer 200.
Docker Hub's `minio/minio` had done the same on 2026-09-11, which is why CI had moved to
quay.io. `tools/ci/pull-images.sh` treats `unauthorized` as a refusal and fails at once, so
the `api` and `full-stack-smoke` jobs (two of the four required checks) failed on every
pull request before running a single test. PR #733 was the first to hit it.

## Definition of done

- [x] Both jobs pull an S3-compatible MinIO server without credentials and pin it, so a
      republished tag cannot change CI underneath us.
- [x] The `api` job's S3 integration tests and the community browser journeys pass on it.

## Steps

- [x] Use Chainguard's public MinIO build (`cgr.dev/chainguard/minio`), pinned by the
      digest of its index (linux/amd64 and linux/arm64); its free tier only publishes
      `:latest`, so a tag would drift.
- [x] It runs as uid 65532 with `/usr/bin/minio` as the entrypoint, so the existing
      `server /data` arguments stay and `/data` becomes a tmpfs it can write.
- [x] Note the second registry in `tools/ci/pull-images.sh`'s header.

## How to verify

```bash
node --test tools/ci-images.test.mjs
```

Then the pull request's own `api` and `full-stack-smoke` jobs: the pull step succeeds and
the S3 tests run.

## Notes

- Considered and not taken: a different S3 server (SeaweedFS, versitygw, LocalStack). The
  community upload uses a presigned POST policy, which not every clone implements, and the
  same MinIO server keeps the tests meaningful.
- Chainguard's image has no shell or curl, so `docker-compose.community.yml` (a healthcheck
  with curl, an `mc` init with `/bin/sh`) needs more than an image swap; filed as
  `2026-09-24-run-the-local-community-storage-without`.
- To bump the pin later, read the current index digest anonymously:
  `curl -s "https://cgr.dev/token?scope=repository:chainguard/minio:pull"` for a token, then
  a HEAD on `https://cgr.dev/v2/chainguard/minio/manifests/latest` with an OCI index
  `Accept` header; the digest is in `Docker-Content-Digest`.
