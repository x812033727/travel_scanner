---
id: 2026-09-28-vps-independent-youtube-upload-service-mode
title: VPS independent YouTube upload service mode
status: in-progress
priority: P1
area: tools
owner: codex-vps-upload
claimed_at: 2026-09-28T04:55:21Z
created_at: 2026-09-28T04:50:52Z
completed_at:
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
- [ ] The website can submit an approved package to the independent service and show progress.
- [ ] Jobs survive service restarts and retries do not duplicate already uploaded videos.
- [ ] Files, title, full description, captions and thumbnail stay bound to the approved package.
- [ ] Authentication failures require owner action; credentials never appear in responses or logs.
- [ ] A standalone deployment package, operating guide and meaningful regression tests exist.

## Steps

- [x] Inspect current upload lifecycle, review-store contracts and concurrent work.
- [x] Resolve the engine question already sent to the owner; then claim and finalize scope.
- [ ] Implement the selected service, website integration and tests.
- [ ] Prepare a draft PR with verified results and explicit deployment requirements.

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
