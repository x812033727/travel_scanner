---
id: 2026-09-24-run-the-local-community-storage-without
title: Run the local community storage without MinIO's login-only images
status: open
priority: P3
area: ops
owner:
claimed_at:
created_at: 2026-09-24T15:12:01Z
completed_at:
branch:
depends_on: []
scope:
  - docker-compose.community.yml
---

# Run the local community storage without MinIO's login-only images

## Why

`docker-compose.community.yml` starts `quay.io/minio/minio` and initialises the bucket with
`quay.io/minio/mc`. Since 2026-09-24 both need a login (Docker Hub's copies since
2026-09-11), so `docker compose -f docker-compose.yml -f docker-compose.community.yml up`
fails for anyone without MinIO credentials. CI moved to Chainguard's public build
(`cgr.dev/chainguard/minio`, task 2026-09-24-pull-minio-for-ci-from-a), but the compose
file cannot take the same image as it is: the healthcheck runs `curl` inside the
container and the init service runs `/bin/sh`, and Chainguard's images carry neither.

## Definition of done

- [ ] The community compose overlay starts storage, creates the private bucket and
      reports healthy with images anyone can pull.

## Steps

- [ ] Choose: Chainguard's `-dev` variants (if the free tier serves them), a healthcheck
      the minimal image can run (`mc ready` from the client image, or the API container
      polling `/minio/health/live`), or creating the bucket from the API container with
      boto3 as `ci.yml` already does.
- [ ] Pin whatever is chosen by digest, as `ci.yml` does.

## How to verify

```bash
docker compose -f docker-compose.yml -f docker-compose.community.yml up -d community-storage community-storage-init
docker compose -f docker-compose.yml -f docker-compose.community.yml ps
```

## Notes

- Found when quay.io started refusing anonymous pulls and blocked PR #733's CI.
