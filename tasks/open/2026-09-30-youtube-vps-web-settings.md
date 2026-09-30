---
id: 2026-09-30-youtube-vps-web-settings
title: Configure the VPS YouTube uploader from video settings
status: review
priority: P1
area: api
owner: codex-vps-web-settings
claimed_at: 2026-09-30T12:14:39Z
created_at: 2026-09-30T12:06:46Z
completed_at:
branch: codex/youtube-vps-web-settings-20260930
depends_on: []
scope:
  - apps/api/app/video_youtube/vps_settings.py
  - apps/api/app/video_youtube/vps.py
  - apps/api/app/video_youtube/admin_api.py
  - apps/api/app/video_youtube/sync.py
  - apps/api/tests/test_video_youtube_vps_settings.py
  - apps/api/tests/test_video_youtube_vps.py
  - apps/api/tests/test_video_youtube_sync.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_youtube.py
  - apps/api/tests/test_video_review_renewal.py
  - apps/api/tests/test_video_reviews_integration.py
  - services/youtube-uploader/src/server.mjs
  - services/youtube-uploader/test/service.test.mjs
  - apps/web/components/admin-video-vps-settings.tsx
  - apps/web/components/admin-video-vps-settings.test.tsx
  - apps/web/components/admin-video-youtube.tsx
  - apps/web/components/admin-video-youtube.test.tsx
  - apps/web/components/admin-video-vps-upload.tsx
  - apps/web/components/admin-video-vps-upload.test.tsx
  - apps/web/lib/video-vps-copy.ts
  - apps/web/lib/video-vps-messages/en.json
  - apps/web/lib/video-vps-messages/zh-TW.json
  - apps/web/lib/video-vps-messages/zh-CN.json
  - apps/web/lib/video-vps-messages/ja.json
  - apps/web/lib/video-vps-messages/ko.json
  - docs/videos/VPS-UPLOADER.md
---

# Configure the VPS YouTube uploader from video settings

## Why

The owner encounters a VPS-not-configured message but has no website form to
configure the uploader. Add a dedicated settings card in the existing video settings
workspace, backed by persisted encrypted configuration that the uploader bridge
actually uses. Service connectivity and Google login must remain distinct states.

## Definition of done

- [x] Video settings exposes an editable VPS connection form to settings managers.
- [x] Saved configuration immediately controls all VPS requests and API/upload guards.
- [x] Secrets are encrypted, never returned, and retained only for the same origin.
- [x] Test connection reports reachability/channel match without claiming Google login.
- [x] A separate remote-desktop link lets the owner complete VPS browser login.
- [x] Changing the connection cannot orphan active uploader jobs or bypass duplicate-upload guards.
- [ ] Five-language UI copy, focused regressions and required local checks pass.

## Steps

- [x] Inspect existing settings, encryption, RBAC and scope/PR collisions.
- [x] Claim a dedicated task on a fresh branch from origin/main.
- [x] Implement persistent backend configuration, runtime resolution and connection test.
- [x] Add the website settings card and links from blocked upload states.
- [x] Add active job counts to the service status endpoint and verify its tests.
- [ ] Validate, independently review, record limitations and open a draft PR.

## How to verify

Run focused API tests for configuration/RBAC, encrypted secrets, stale writes,
environment fallback, channel mismatch and active-job protection. Run the uploader
service tests, focused web component tests, web lint/typecheck/i18n and task checks.
Inspect the settings card on the local website. Do not submit a real upload to test
the form. Deployment, live settings changes and Google login require their own
execution and acceptance; they are not completion claims for this code change.

## Notes

- The old fixed message is triggered by an empty environment URL, not a failed
  Google login. `/status` previously returned worker idle even for needs_action jobs.
- The existing YouTube OAuth card is already a dedicated settings owner storing
  encrypted credentials. VPS settings likewise have one dedicated editable owner.
- `apps/web/messages` is claimed by an active task. This change uses the repository's
  existing typed `lib/*-copy.ts` plus five JSON catalogs pattern without editing that
  claimed directory or force-releasing another agent's work.
- The settings card is attached through `admin-video-youtube.tsx`; it does not edit
  `admin-video-reviews.tsx`, which is being changed by another open PR.
- A necessary session argument is added only to `_short_revision_allowed` and its
  caller in video_reviews/admin_service.py. Two open PRs touch other functions in
  that file; no active task owns it. Recheck those diffs before PR creation.
- Previous backfill receipts and the independent approved-language-sync task remain
  untracked work from earlier turns; keep them out of this feature's commit.
- No production containers, settings, secrets, Google accounts or YouTube uploads
  are changed by this implementation task.
- Independent review found and resolved a project/config lock-order inversion and
  invalid-environment GET/test failures. An authenticated empty old queue also
  permits correcting a mistyped channel; connection tests still require a match.
- API regressions: 152 passed, 7 skipped (PostgreSQL integration environment absent).
  Full API ruff, mypy app (445 files) and mypy tests (336 files) passed.
- Frontend focused regressions: 47 passed; full web lint and typecheck passed.
  Five-locale namespace validation passed; separate VPS catalog key alignment is
  covered by component tests. Tool suite: 951 passed, 2 skipped. Uploader service
  suite: 13 passed in the delegated run (11 service tests rechecked by root).
- Local website/browser acceptance remains unverified: the local mock API and
  Next server started, but IAB attachment/focus commands repeatedly timed out.
  No form save, connection-test action or screenshot was completed in the browser.
  Do not interpret component tests or mock health checks as visual/live acceptance.
- The remaining local browser acceptance is tracked in
  `2026-09-30-youtube-vps-web-settings-browser-acceptance`. Real service deployment,
  Google login and private-upload acceptance remain in the existing ops task
  `2026-09-28-vps-youtube-studio-deployment-and-live`.
