---
id: 2026-09-30-youtube-vps-web-settings-browser-acceptance
title: Verify the VPS settings card in desktop and mobile browsers
status: done
priority: P2
area: web
owner: claude-opus-5-5-vps-settings-e2e
claimed_at: 2026-10-05T01:19:29Z
created_at: 2026-09-30T12:42:30Z
completed_at: 2026-10-05T04:13:01Z
branch: claude/vps-settings-e2e
depends_on:
  - 2026-09-30-youtube-vps-web-settings
scope:
  - docs/videos/vps-web-settings-acceptance
  - apps/web/e2e/admin-video-vps-settings.spec.ts
  - tools/e2e-runtime-api.mjs
  - .github/workflows/ci.yml
  - apps/web/components/admin-video-vps-settings.tsx
  - apps/web/components/admin-video-vps-settings.test.tsx
---

# Verify the VPS settings card in desktop and mobile browsers

## Why

The website VPS settings feature has component and API regression coverage, but
local browser acceptance could not finish because IAB attachment and focus commands
repeatedly timed out. Verify the rendered card and its real Next/BFF requests using
an isolated local mock before treating the UI as visually accepted.

## Definition of done

- [x] Desktop and mobile layouts show the card without clipping or horizontal overflow.
- [x] Save, reload, test success/failure and stale-write recovery work through the local BFF.
- [x] Read-only users cannot save/test; saved secrets never appear in the page or evidence.
- [x] The saved desktop link and unconfigured uploader settings link lead to the intended pages.
- [x] Screenshots and observed request/result evidence are saved in the scoped receipt folder.

## Steps

- [x] Start the unchanged runtime mock plus a local proxy for the new settings routes.
- [x] Run the site with API_INTERNAL_URL pointing only to the local proxy.
- [x] Sign in with a synthetic fixture, inspect both viewports and exercise the form.
- [x] Record acceptance and shut down only the test servers created for this run.

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
- 2026-10-01 local attempt on `76b39a25e3819d5ef97648e10a5b8c6bb1bfbd74`:
  production `next build` passed with Node 24.21.0, but automatic approval review
  rejected the hidden Next startup command with `blocked by policy` before it
  executed. No alternate launcher was tried; browser assertions and screenshots
  remain unexecuted. The owned fixture/proxy processes were stopped and ports
  18780, 18781 and 3016 were confirmed without listeners. See
  [the attempt receipt](../../docs/videos/vps-web-settings-acceptance/README.md).
  Prepared private helpers are syntax-checked only; all browser DoD items remain
  open. This is neither a product failure nor successful visual acceptance.
- 2026-10-05 (claude-opus-5-5-vps-settings-e2e, branch `claude/vps-settings-e2e`):
  the acceptance is now `apps/web/e2e/admin-video-vps-settings.spec.ts`, six cases on
  `desktop-chromium` and `mobile-chromium`, added to the isolated browser job in
  `.github/workflows/ci.yml` (whose screenshot artifact now also keeps
  `youtube-vps-settings-*.jpg`). Instead of a private proxy, "the local proxy" of the
  Steps is a synthetic settings store in `tools/e2e-runtime-api.mjs` (the
  `API_INTERNAL_URL` Playwright already starts), keyed per test by a `?fixture=` query
  the spec adds, so the card's requests cross the real BFF. Scope grew by those three
  files and by the card and its unit test (below).
- Found and fixed: the uploader's "設定 VPS 服務" link opened the settings tab with the
  card out of view (viewport ratio 0 on both projects), because the tab renders on the
  client after the browser's fragment jump. The card now scrolls itself into view once
  when its settings first arrive and the URL names its fragment; unit test added, and
  the e2e asserts the heading is in the viewport.
- Local evidence on a webpack build (Turbopack refuses the linked `node_modules`):
  12/12 in the receipt run and 24/24 with `--repeat-each=2`, with the spec's own
  timeouts (60 s for the two cases with two full renders, 30 s for the rest) on a
  machine at 100 % CPU. Negative checks: a store that echoes the secret fails the
  secret assertions; without the scroll fix the link case and the unit test fail.
  Screenshots, observed requests and `attempt-20261005.json` are in
  `docs/videos/vps-web-settings-acceptance/`; the README there marks CI as pending
  until this PR's `web-e2e` run is green.
- Review round 1 (same owner): the synthetic store kept a test's `browser_status` and
  `active_jobs` and sent them back on every later read, so the first layout screenshots
  showed "背景工作狀態: 閒置" and "進行中的工作: 0" after a page load. The API never
  stores them (`view()` leaves both null; only `test_connection`'s answer adds them
  through `model_copy(update=details)`). The store now does the same, the layout case
  asserts a page load shows neither (a store with the old behaviour fails it on both
  projects), and the screenshots, observed requests and receipt hashes were regenerated:
  12/12 and 24/24 again, this time against this checkout's fixture on its own port
  (`E2E_API_PORT=18800`, `API_INTERNAL_URL`), because Playwright reuses whatever fixture
  already listens on the shared `:8000`.
- Not repeated here: a read-only role's direct API write is refused by the API
  (`test_settings_routes_apply_explicit_read_and_manage_permissions`); the spec checks
  that the UI sends no write. Real VPS, Google login, uploads and deployment stay with
  `2026-09-28-vps-youtube-studio-deployment-and-live`.
