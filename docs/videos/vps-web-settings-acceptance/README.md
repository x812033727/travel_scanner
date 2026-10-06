# VPS web settings browser acceptance

Status on 2026-10-05: **accepted in an isolated local browser run; the CI run of
the same spec is the proof that counts and is pending on the pull request that
adds this receipt.** Until that pull request's `web-e2e` job is green, treat the
CI column below as unproven.

The acceptance is now a Playwright spec instead of a one-off manual session:
[`apps/web/e2e/admin-video-vps-settings.spec.ts`](../../../apps/web/e2e/admin-video-vps-settings.spec.ts),
listed in the isolated browser job of `.github/workflows/ci.yml`, so it runs on
every pull request in both projects of `apps/web/playwright.config.ts`
(`desktop-chromium` and `mobile-chromium`, a Pixel 7).

## What the requests go through

- The page is the real Next app (`/zh-TW/admin/videos?tab=settings#youtube-vps-settings`),
  rendered by the server with the isolated administrator bootstrap from
  `tools/e2e-runtime-api.mjs` (`e2e-session` is the owner, `e2e-viewer` the read-only role).
- The card's own reads, saves and connection tests leave the browser, cross the real
  same-origin BFF (`apps/web/app/api/travel/[...path]/route.ts`: mutation origin check,
  cookie forwarding, status and body passthrough, including the 409) and reach a
  synthetic store in `tools/e2e-runtime-api.mjs`. That store answers the way
  `apps/api/app/video_youtube/vps_settings.py` does where the card can tell: the
  secret is write-only, unknown fields are a 422, a stale `expected_updated_at` is a
  409, a save clears the last test, and a connection test answers 200 with its
  verdict and a new revision. Like the API, it never stores the background status
  and job count: `view()` leaves both null, and only the answer to a test that
  reached the service carries them (`test_connection`'s `model_copy(update=details)`),
  so a page load never shows them. It forwards nothing anywhere.
- The spec's route handler adds `?fixture=<project, test, attempt>` to those requests
  so the parallel desktop and mobile runs never share a revision. That query string
  is the only difference from what the card sends in production.
- "Another administrator" (the stale-write case, and seeding) is the same BFF called
  through Playwright's request context with the owner session and an `Origin` header.
- The video page's project, the YouTube connection and the per-video uploader status
  are browser-route fixtures, as in `admin-video-manual-upload.spec.ts`. The automation
  settings section under the card is answered 503 and shows its own load error; it has
  its own tests and is outside this acceptance.
- Every other origin is aborted and recorded; each case asserts none was requested.
  The saved desktop link's loopback page is answered with a synthetic HTML page.

All values are synthetic: service `http://127.0.0.1:18781`, desktops
`http://127.0.0.1:16080/vnc.html` and `:16081`, channel IDs `UCSyntheticFixture00000N`,
and secrets that say `synthetic-e2e-secret-not-real`.

## Cases and evidence

| Definition of done | Case in the spec | Local 2026-10-05 | CI |
| --- | --- | --- | --- |
| Desktop and mobile layouts, light and dark, no clipping or horizontal overflow | "a configured and tested card fits…": a page load after another administrator's successful test, which shows the stored verdict and, as asserted, no background status or job count (and the empty card at the start of the save case, without screenshots) | passed, both projects; screenshots below | pending |
| Save, reload | "an owner saves and reloads…": first save sends every field with `expected_updated_at: null`; after a reload the URL, channel, desktop and switch persist and the password field is empty with the "kept" placeholder | passed | pending |
| Test failure and success | "a connection test fails on a mistyped channel…": failed alert and reason, the test button stays off while the edit is unsaved, the correction sends only `channel_id` at the revision the test left, then success with background status idle and 0 jobs | passed | pending |
| Stale-write recovery | "a stale save keeps the edits…": another administrator changes the desktop address; the card's save gets 409 and keeps the edited channel and secret; refresh takes the new desktop address and keeps both edits; the retry sends only `channel_id`, `secret` and the new revision | passed | pending |
| Read-only users cannot save or test | "a read-only administrator…": note shown, every field and the save and test buttons disabled, refresh works, zero writes | passed | pending |
| Saved secret never in the page or evidence | every case: no administrator API response, page HTML or receipt file contains either synthetic secret; responses carry `secret_set` only | passed | pending |
| Saved desktop link | the connection-test case: `href` is the saved loopback desktop, `target="_blank"`, `rel` has `noopener`; clicking opens that page in a new tab | passed | pending |
| Unconfigured uploader's settings link | "an unconfigured uploader links…": from the video page's VPS panel to `?tab=settings#youtube-vps-settings`, with the card's heading in the viewport | passed after the fix below | pending |

Committed evidence, all from the local run:

- `youtube-vps-settings-{desktop,mobile}-chromium-tested-{light,dark}.jpg`: the card
  as a page load shows it after a successful synthetic connection test (the verdict,
  its message and time, no background status or job count), clipped from a
  full-page capture.
- `observed-requests-{desktop,mobile}-chromium.json`: each case's settings requests
  as the browser saw them (method, path, status, fields sent with the secret replaced
  by a placeholder, and the non-secret fields received). Seeding and "another
  administrator" calls go through the request context and are not in these files.
- [`attempt-20261005.json`](attempt-20261005.json): environment, commands, counts and
  hashes of the files the run used.

Regenerate them with `VPS_ACCEPTANCE_DIR=<absolute path of this folder>` set for a
run of the spec; without it, CI writes the screenshots under `test-results` and keeps
them for three days as the `youtube-manual-browser-evidence-*` artifact. Playwright
reuses any runtime fixture already listening on `127.0.0.1:8000`, so on a machine
shared with other checkouts start this checkout's fixture on its own port
(`E2E_API_PORT`) and point `API_INTERNAL_URL` at it, as the rerun in
`attempt-20261005.json` did.

## Found and fixed during acceptance

Following the uploader's settings link landed on the settings tab with the VPS card
out of view (viewport ratio 0 on both projects): the tab renders on the client, after
the browser's own fragment jump found nothing. `YoutubeVpsSettingsCard` now scrolls
itself into view once, when its settings first arrive and the URL names its fragment
(unit test in `apps/web/components/admin-video-vps-settings.test.tsx`).

Review of the first receipt found a fixture error, not a product one: the synthetic
store kept a test's background status and job count and sent them back on every later
read, so the first screenshots showed "背景工作狀態: 閒置" and "進行中的工作: 0" after a
page load, a state the API cannot produce. The store now adds them to the test's own
answer only, the layout case asserts a page load shows neither, and the screenshots,
observed requests and hashes were regenerated.

## Limits

- The local run used a webpack production build (`next build --webpack`): Turbopack
  refuses this machine's linked `node_modules` ("points out of the filesystem root").
  CI builds with the default bundler.
- This Windows ARM64 machine ran at 100 % CPU with other agents' builds and tests
  during the run. The two cases with two full server renders (save and reload, and
  the uploader link) carry `test.setTimeout(60_000)`, as other admin acceptance specs
  do; locally the first of them took up to 43 s. The other four keep the default
  30 s. Before the read-only case dropped a layout pass the layout case already makes,
  it timed out once in 24 local repeats (an 8.5 s browser start and an 8 s stalled
  page evaluation). The final spec passed 12 of 12 in the receipt run and 24 of 24
  repeated twice, both in the first run and in the rerun after the review correction
  above (where the first case took up to 29 s). Whether these budgets hold on CI's
  runners is what the pending CI run shows.
- The synthetic store copies the API's rules; the rules themselves are proven by
  `apps/api/tests/test_video_youtube_vps_settings.py` (including
  `test_settings_routes_apply_explicit_read_and_manage_permissions` for direct writes
  by a read-only role, which this spec does not repeat).
- Not covered here, and not claimed: a real VPS, Google login, channel identity, real
  uploads, production deployment and owner review. Those stay with
  `2026-09-28-vps-youtube-studio-deployment-and-live`.

The blocked 2026-10-01 attempt is kept as [`attempt-20261001.json`](attempt-20261001.json).
