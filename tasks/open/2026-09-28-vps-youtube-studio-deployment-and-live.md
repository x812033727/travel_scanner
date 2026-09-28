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
branch:
depends_on:
  - 2026-09-28-vps-independent-youtube-upload-service-mode
scope:
  - services/youtube-uploader/src/studio.mjs
  - ops/youtube-uploader
  - docs/videos/VPS-UPLOADER.md
---

# VPS YouTube Studio deployment and live private upload acceptance

## Why

The independent uploader and site mode are implemented, but no production VPS or Google
account was accessed. Synthetic DOM tests cannot confirm today's signed-in Studio selectors,
Google login eligibility, caption replacement or real media processing.

## Definition of done

- [ ] Owner identifies the VPS and approves its deployment and a specific private test video.
- [ ] Standalone Docker build and headful desktop startup pass in CI and on the chosen host.
- [ ] Owner logs in and confirms the exact channel; no secrets/cookies are copied into evidence.
- [ ] Real private upload, metadata, thumbnail, captions and translations persist after reload.
- [ ] Existing videos and interrupted jobs resume without a second MP4 upload.
- [ ] Desktop/mobile admin progress is visually checked and receipt recording is verified.

## Steps

- [ ] Read docs/videos/VPS-UPLOADER.md; follow production deploy/host skills if using mokaair.com.
- [ ] Obtain missing host/version/test-video decisions before any production mutation.
- [ ] Verify live Studio DOM, update selectors/flow only from observations, and add sanitized fixtures.
- [ ] Run the documented acceptance matrix and record exact versions/results.

## How to verify

Use the setup and final acceptance sections in docs/videos/VPS-UPLOADER.md.
Run service tests, focused API/UI tests, i18n/typecheck and independent container CI.
Confirm the persistent private video ID and each applied asset; HTTP health alone is insufficient.

## Notes

- Browser engine was confirmed by the owner. Implementation authorization did not include a
  production deployment, Google login or a real test upload. No host credentials were requested.
- Uploader defaults to loopback, a dedicated persistent profile and private videos. API and
  service share only a file-mounted service secret; Google OAuth/cookies are not transferred.
- Local machine has no Docker command. Container build/startup is covered by the dedicated
  GitHub Actions workflow; record its actual result before calling the deployment package verified.
- Local Playwright tested only intercepted synthetic pages. Exact Studio selectors remain
  provisional until owner-assisted acceptance; an unexpected page pauses the durable job.
