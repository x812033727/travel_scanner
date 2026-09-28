---
id: 2026-09-28-youtube-manual-browser-validation
title: Verify manual YouTube upload guide on desktop and mobile
status: in-progress
priority: P2
area: web
owner: codex-pr-merge-watch
claimed_at: 2026-09-28T04:54:04Z
created_at: 2026-09-28T04:23:22Z
completed_at:
branch: codex/pr890-browser-validation
depends_on:
  - 2026-09-28-youtube-manual-upload
scope:
  - docs/videos/MANUAL-UPLOAD.md
  - apps/web/e2e/admin-video-manual-upload.spec.ts
  - .github/workflows/ci.yml
---

# Verify manual YouTube upload guide on desktop and mobile

## Why

The manual upload guide has component coverage, but interactive desktop/mobile visual
validation could not complete: Chrome create/get-tab calls repeatedly timed out during local
preview, while the host had about 0.26 GiB available memory. Do not count the attempted preview
as a browser pass or a real YouTube upload.

## Definition of done

- [ ] Desktop and narrow mobile views show all five steps without horizontal overflow.
- [ ] Switching language, copying full descriptions, downloading the correctly named caption
      and thumbnail, and returning to the edited API form work in a real browser.
- [ ] Save screenshots and record the browser/viewport and fixture used in MANUAL-UPLOAD.md.

## Steps

- [ ] Start an isolated local API fixture and web preview of codex/youtube-manual-upload.
- [ ] Exercise a new video and a failed sync with an existing video ID.
- [ ] Record visual evidence; keep real production/YouTube changes outside this task.

## How to verify

Open /zh-TW/admin/videos?video=<fixture>, enter manual mode, select each language and copy
the description. Verify the retained chapters, each caption's language and file extension,
and the existing-video Studio link. Resize to a narrow mobile viewport and check each step.

## Notes

- Merge watcher claimed this unowned follow-up on a separate branch from PR #890.
  No other active local task owns these exact paths. Local free memory is still
  below 0.5 GiB, so browser validation will use the existing CI production build
  and Chromium projects, with synthetic API fixtures and a small screenshot artifact.
  Screenshots and successful browser execution are still pending; adding tests alone
  is not a visual-validation receipt.
- Added 20 isolated Chromium cases (five UI languages, new/existing video, desktop/mobile)
  with real clipboard reads and download events, preserved form edits, no site writes or
  external requests, light/dark overflow checks and eight small Traditional Chinese screenshots.
- Scoped ESLint, Playwright `--list` (20 cases), task validation (958 files), workflow YAML
  and `git diff --check` pass. Full local TypeScript checking exhausted its 768 MiB heap
  while the host had about 0.5 GiB free. It did not pass; full typecheck and browser execution
  must be verified in CI before this task can close.

- The temporary local fixture generator is outside Git in this chat's visualization directory
  as manual-preview-server.mjs. It serves synthetic data on 127.0.0.1:18943; web used 18944.
- Its fixture-login endpoint only creates the synthetic e2e-session local cookie.
- Both preview processes were stopped after failed browser attempts. Generated next-env.d.ts
  changes were restored. No production hosts, Google credentials or real YouTube state changed.
