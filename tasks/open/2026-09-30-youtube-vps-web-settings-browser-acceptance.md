---
id: 2026-09-30-youtube-vps-web-settings-browser-acceptance
title: Verify the VPS settings card in desktop and mobile browsers
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-30T12:42:30Z
completed_at:
branch:
depends_on:
  - 2026-09-30-youtube-vps-web-settings
scope:
  - docs/videos/vps-web-settings-acceptance
---

# Verify the VPS settings card in desktop and mobile browsers

## Why

The website VPS settings feature has component and API regression coverage, but
local browser acceptance could not finish because IAB attachment and focus commands
repeatedly timed out. Verify the rendered card and its real Next/BFF requests using
an isolated local mock before treating the UI as visually accepted.

## Definition of done

- [ ] Desktop and mobile layouts show the card without clipping or horizontal overflow.
- [ ] Save, reload, test success/failure and stale-write recovery work through the local BFF.
- [ ] Read-only users cannot save/test; saved secrets never appear in the page or evidence.
- [ ] The saved desktop link and unconfigured uploader settings link lead to the intended pages.
- [ ] Screenshots and observed request/result evidence are saved in the scoped receipt folder.

## Steps

- [ ] Start the unchanged runtime mock plus a local proxy for the new settings routes.
- [ ] Run the site with API_INTERNAL_URL pointing only to the local proxy.
- [ ] Sign in with a synthetic fixture, inspect both viewports and exercise the form.
- [ ] Record acceptance and shut down only the test servers created for this run.

## How to verify

Use `/zh-TW/admin/videos?tab=settings#youtube-vps-settings`, a clearly synthetic
channel/secret and loopback service/desktop URLs. Reload after a successful save;
confirm the password field is empty and unchanged connection fields persist.
Test only a mock service. Inspect rendered light/dark desktop and mobile layouts.
Production deployment, Google login and real upload remain under the existing
`2026-09-28-vps-youtube-studio-deployment-and-live` task and owner authorization.

## Notes

- The implementation run started mock ports 18740/18741 and Next 18742, but no
  browser form submission or screenshot completed. All three servers were stopped.
- Scratch proxy scripts remain outside the repo in this chat's local visualization
  directory under `vps-preview`; reconstruct a small proxy if that local artifact
  is unavailable. It must never forward to a production origin.
- Reacquiring the same browser binding or attempting new tabs did not repair the
  attachment/focus failure. Wait for an attached active tab before resuming UI work.
- Do not put real channel credentials, cookies or service secrets in the receipt.
