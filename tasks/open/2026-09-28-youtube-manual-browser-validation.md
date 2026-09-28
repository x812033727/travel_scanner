---
id: 2026-09-28-youtube-manual-browser-validation
title: Verify manual YouTube upload guide on desktop and mobile
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-28T04:23:22Z
completed_at:
branch:
depends_on:
  - 2026-09-28-youtube-manual-upload
scope:
  - docs/videos/MANUAL-UPLOAD.md
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

- The temporary local fixture generator is outside Git in this chat's visualization directory
  as manual-preview-server.mjs. It serves synthetic data on 127.0.0.1:18943; web used 18944.
- Its fixture-login endpoint only creates the synthetic e2e-session local cookie.
- Both preview processes were stopped after failed browser attempts. Generated next-env.d.ts
  changes were restored. No production hosts, Google credentials or real YouTube state changed.
