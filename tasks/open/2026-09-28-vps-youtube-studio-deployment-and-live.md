---
id: 2026-09-28-vps-youtube-studio-deployment-and-live
title: VPS YouTube Studio deployment and live private upload acceptance
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-09-28T05:42:23Z
completed_at:
branch: codex/youtube-vps-uploader
depends_on:
  - 2026-09-28-vps-independent-youtube-upload-service-mode
scope:
  - services/youtube-uploader/src/studio.mjs
  - ops/youtube-uploader
  - docs/videos/VPS-UPLOADER.md
  - docker-compose.prod.yml
  - .github/workflows/youtube-uploader.yml
---

# VPS YouTube Studio deployment and live private upload acceptance

## Why

The independent uploader and site mode are implemented. The owner selected mokaair.com;
only read-only host preflight has run, and no Google account was accessed.
Synthetic DOM tests cannot confirm today's signed-in Studio selectors,
Google login eligibility, caption replacement or real media processing.

## Definition of done

- [x] Owner identifies the VPS: mokaair.com production host.
- [ ] Owner approves the exact deployment steps/version and a specific private test video.
- [ ] Standalone Docker build and headful desktop startup pass in CI and on the chosen host.
- [ ] Owner logs in and confirms the exact channel; no secrets/cookies are copied into evidence.
- [ ] Real private upload, metadata, thumbnail, captions and translations persist after reload.
- [ ] Existing videos and interrupted jobs resume without a second MP4 upload.
- [ ] Desktop/mobile admin progress is visually checked and receipt recording is verified.

## Steps

- [x] Read docs/videos/VPS-UPLOADER.md and the production deploy/host/release skills.
- [ ] Obtain missing host/version/test-video decisions before any production mutation.
- [ ] Verify live Studio DOM, update selectors/flow only from observations, and add sanitized fixtures.
- [ ] Run the documented acceptance matrix and record exact versions/results.

## How to verify

Use the setup and final acceptance sections in docs/videos/VPS-UPLOADER.md.
Run service tests, focused API/UI tests, i18n/typecheck and independent container CI.
Confirm the persistent private video ID and each applied asset; HTTP health alone is insufficient.

## Notes

- Read-only host preflight at 2026-09-28 06:17-06:19 UTC: no hold, deploy lock free,
  clean live HEAD 2fa7bf1e; 4 CPUs, 15,987 MiB total RAM / 13,282 MiB available,
  91 GiB disk free; Docker 29.1.3, Compose 2.40.3. Ports 8789 and 6080 unused.
  Existing .env remains 0600 root:root. No production files, settings or containers changed.
- These are point-in-time observations; repeat preflight before an approved deployment.
- Same-host integration must survive the normal site deploy script's single production
  Compose file and preserve the uploader's separate project/profile/data volume.
- Scope expanded after checking local/remote branches, active task claims and all 11 open
  PRs: none of the other 10 PRs changes docker-compose.prod.yml; no active task owns it.
- Same-host preparation adds the API-only internal RPC network, read-only secret directory,
  separate uploader overlay and CI client checks before/after recreation. Local workflow
  checks: 8 passed, 1 Bash/temp-path suite skipped on Windows; task check: 964 validated.
  Docker is unavailable locally; same-host startup/permissions must pass the dedicated CI.
- Commit 24424d4a passed standalone Docker Compose build and headful/noVNC/HTTP startup
  in workflow 36386376526. This predates the same-host overlay and does not prove live upload.
- Awaiting owner approval for merge, guarded site deployment/backup, secret provisioning,
  independent container startup and site .env/API activation. No production writes performed.
- Browser engine was confirmed by the owner. Implementation authorization did not include a
  production deployment, Google login or a real test upload. No host credentials were requested.
- Uploader defaults to loopback, a dedicated persistent profile and private videos. API and
  service share only a file-mounted service secret; Google OAuth/cookies are not transferred.
- Local machine has no Docker command. Container build/startup is covered by the dedicated
  GitHub Actions workflow; record its actual result before calling the deployment package verified.
- Local Playwright tested only intercepted synthetic pages. Exact Studio selectors remain
  provisional until owner-assisted acceptance; an unexpected page pauses the durable job.

### 2026-09-29 看板盤點與站主決定

站主回覆「依賴就緒後準備試作／上傳驗收方案」。目前依賴與可執行步驟見docs/work-status-2026-09-29-video-acceptance-plan.md；未部署、生成、登入或上傳。

本次僅追加交接證據，不改既有owner、scope、branch或執行狀態。
