---
id: 2026-10-05-deploy-skill-says-unchanged-services-keep
title: Deploy skill says unchanged services keep their containers, but every deploy recreates all of them; preflight checks paid video work
status: in-progress
priority: P2
area: tools
owner: claude-opus-5.5
claimed_at: 2026-10-05T03:40:54Z
created_at: 2026-10-05T03:40:42Z
completed_at:
branch: claude/deploy-recreates-all
depends_on: []
scope:
  - .agents/skills/deploy
  - .claude/skills/deploy
---

# Deploy skill says unchanged services keep their containers, but every deploy recreates all of them; preflight checks paid video work

## Why

The deploy of 363489fe9 (PR #1245) on 2026-10-05 03:32Z touched only `.agents/skills/deploy` and
`tasks/`. Even so, its log (`/root/deploy-logs/deploy_20261005_033250.log`) shows `Recreate` for every
container except postgres and redis: migrate, api, worker, alert-*, analytics-scheduler,
community-sweeper, hotspot-collector, news-*, web, video-ai-worker and video-worker. SKILL.md said
「內容沒變的服務沿用舊容器」, and the host-verify.sh comment said a docs-only commit leaves api and
web as they were. A reader who believes that may deploy over a paid model call that is in flight;
`docs/videos/recovery/2026-10-04-stalled-media.md` forbids that. runbook.md already said all
containers are rebuilt, so the docs contradicted each other.

## Definition of done

- [x] SKILL.md (and its byte-identical `.claude` copy), runbook.md, post-deploy.md and the
      host-verify.sh comment say that every deploy recreates every container built from the repo, and why.
- [x] `host-preflight.sh` reports open video stage and media jobs in its default mode, and prints
      `PAID WORK IN FLIGHT` for a running stage job; preflight.md explains each status.

## Steps

- [x] Find the cause on the host, read-only.
- [x] Correct the docs and the comment.
- [x] Add the paid-work section to the preflight script and run it on the host.
- [ ] `npm run test:tools`, open a PR.
- [ ] After it merges: deploy, run the new preflight first and `host-verify.sh` after, record the
      result here and close the task in a tasks-only PR.

## How to verify

```bash
bash -n .agents/skills/deploy/scripts/host-preflight.sh
cmp .agents/skills/deploy/SKILL.md .claude/skills/deploy/SKILL.md
npm run test:tools
MSYS_NO_PATHCONV=1 <SSH> -m .agents/skills/deploy/scripts/host-preflight.sh   # ends with "-- paid video work --"
```

## Notes

- Cause: the deploy script runs plain `compose up --build -d`, with no `--force-recreate`. On a
  full cache hit the image keeps its `Created` time (both api images: 02:10:44.89Z), but the id
  still changed from `67929f47…` to `9e5d4be0…`. The host runs Docker 29.1.3 with the containerd
  image store (`driver-type io.containerd.snapshotter.v1`). Its image id is the digest of an OCI
  image index (`Descriptor.mediaType application/vnd.oci.image.index.v1+json`, size 856), which
  changes with every build. Compose recreates any container whose image id moved.
- Not changed: the host-verify started-time checks still compare against the last commit that
  touched each build context. They would stay right if image ids ever become stable (for example
  if buildx or attestations change).
- Paid work: a `running` stage job turns `uncertain` when its process dies
  (`app/video_automation/run_jobs.py`), so that alone blocks a deploy. Media jobs keep their state in
  the DB and the next poll resumes them, without asking the vendor twice (`app/video_media/jobs.py`),
  so they are printed but do not block.
- The two psql selects ran in auto mode through `plink -m` without a classifier refusal on
  2026-10-05, both inside a verify run and as the final preflight. Both lines printed `none`.
