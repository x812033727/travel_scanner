---
id: 2026-09-28-vps-independent-youtube-upload-service-mode
title: VPS independent YouTube upload service mode
status: done
priority: P1
area: tools
owner: codex-vps-upload
claimed_at: 2026-09-28T04:55:21Z
created_at: 2026-09-28T04:50:52Z
completed_at: 2026-09-28T05:59:36Z
branch: codex/youtube-vps-uploader
depends_on:
  - 2026-09-28-youtube-manual-upload
scope:
  - services/youtube-uploader
  - ops/youtube-uploader
  - docs/videos/VPS-UPLOADER.md
  - apps/api/app/video_youtube/vps.py
  - apps/api/app/video_youtube/admin_api.py
  - apps/api/app/video_youtube/sync.py
  - .github/workflows/youtube-uploader.yml
  - apps/api/tests/test_video_youtube_vps.py
  - apps/web/components/admin-video-vps-upload.tsx
  - apps/web/components/admin-video-vps-upload.test.tsx
  - apps/web/components/admin-video-youtube.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
---

# VPS independent YouTube upload service mode

## Why

The owner requested an additional upload mode backed by an independent VPS service,
alongside the existing API synchronization and manual Studio guide. The request follows
quota exhaustion; moving an API client to another host alone does not increase its quota.

## Definition of done

- [x] The owner selects the upload engine: browser-operated Studio.
- [x] The website can submit an approved package to the independent service and show progress.
- [x] Jobs survive service restarts and retries do not duplicate already uploaded videos.
- [x] Files, title, full description, captions and thumbnail stay bound to the approved package.
- [x] Authentication failures require owner action; credentials never appear in responses or logs.
- [x] A standalone deployment package, operating guide and meaningful regression tests exist.

## Steps

- [x] Inspect current upload lifecycle, review-store contracts and concurrent work.
- [x] Resolve the engine question already sent to the owner; then claim and finalize scope.
- [x] Implement the selected service, website integration and tests.
- [x] Prepare a draft PR with verified results and explicit deployment requirements.

## How to verify

Run the service tests against fake upstream responses or a local UI fixture; cover
interrupted uploads, restart recovery, duplicate submission, missing files, authentication
loss and permission checks. Verify website mode selection and progress without publishing
real videos. Record exact commands once the engine and runtime are selected.

## Notes

- Worktree: youtube-manual-upload, reused after finishing manual-mode implementation.
  Branch starts at b85f85c4 and includes manual mode from draft PR #890; keep its PR separate.
- The owner confirmed Studio browser mode. Build a separately deployed service, private uploads,
  durable jobs, owner-assisted login and explicit recovery after an uncertain upload.
  Site-to-VPS asset transfer is resumable; once queued, Studio work runs independently.
  No production deployment or real test upload is authorized by this implementation request.
- Existing sync.py runs an asyncio task in the API process because only that container
  mounts the review store. It leases video_projects.youtube_sync, checkpoints resumable
  upload state and skips captions already uploaded. Reuse these contracts where applicable.
- read_package verifies metadata.json against the approved review hash and checks file roles.
  Compilation MP4 uses the existing separate full-video download path.
- Local branches, remote youtube/upload branches, open tasks and open PRs were inspected.
  PR #870 changes review/automation UI and metadata packaging; avoid its component scopes.
  Recheck collisions and update this provisional scope before implementation.
- Official references checked 2026-09-28:
  https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits
  https://developers.google.com/youtube/v3/guides/using_resumable_upload_protocol
  https://www.youtube.com/static?template=terms
  API quotas are project-based; Studio automation is subject to YouTube's automated-access
  restrictions and must not be described as an officially supported unlimited API.
- No production host was accessed, and no credentials, login state or YouTube content changed.
- Draft PR #893 is stacked on #890. The latest manual-mode branch was merged locally to
  include its separate browser-validation work; there were no merge conflicts.
- Implemented immutable manifests, 4 MiB offset transfers, SHA-256 checks, SQLite recovery,
  a single persistent browser, private-only DOM operations, API/VPS exclusion and result recording.
  Restarts cannot silently create another video. Cancelled jobs inherit manually recorded site
  video IDs on resume; unknown old uploads can be reconciled and cancelled without running them.
- Standalone tests: 10 queue/HTTP/recovery tests and 2 intercepted Chromium DOM tests passed.
  The DOM suite validates privacy/channel guards, field replacement, saved text, ambiguity
  and login/challenge stops; it does not prove live Studio compatibility.
- API: existing YouTube/OAuth/sync plus initial VPS suite passed 49 tests; the expanded final
  VPS suite passed 8 tests. Scoped ruff and mypy app/video_youtube plus the VPS test file passed.
- Web: 27 focused VPS/manual/existing YouTube tests passed before the final recovery refinements.
  Scoped ESLint and five-locale i18n validation passed. Final focused rerun and full CI status
  are recorded in PR #893. Local full TypeScript checking was stopped after sustained paging
  on a host with roughly 0.2-0.5 GiB free; it is not recorded as a local pass.
- Commit 0b105dc3 passed the dedicated uploader CI, including npm test, Docker build and
  Xvfb/noVNC/HTTP startup: actions/runs/36383247014. Later code changes require fresh CI.
  The local host has no Docker CLI. Task validation and git diff --check passed.
- Production deployment, owner login, real selectors/private upload acceptance and visual admin
  QA remain in tasks/open/2026-09-28-vps-youtube-studio-deployment-and-live.md. This closes
  implementation only. No merge, activation or publication has occurred.
