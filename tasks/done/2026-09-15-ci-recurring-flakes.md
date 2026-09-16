---
id: 2026-09-15-ci-recurring-flakes
title: Stop the recurring CI flakes: image pulls, keep-alive resets, offline catch-up, disposed route bodies, success artifacts
status: done
priority: P1
area: ops
owner: claude-opus-5
claimed_at: 2026-09-15T06:35:01Z
created_at: 2026-09-15T06:34:53Z
completed_at: 2026-09-16T06:12:32Z
branch: claude/ci-flake-fixes
depends_on: []
scope:
  - .github/workflows/ci.yml
  - .github/workflows/travel-discovery.yml
  - .github/workflows/planner-premium.yml
  - .github/workflows/food-map-reservations.yml
  - tools/ci
  - tools/ci-images.test.mjs
  - apps/web/package.json
  - apps/web/e2e/site-pages.spec.ts
  - apps/web/e2e/community.spec.ts
  - apps/web/components/community/provider.tsx
  - apps/web/components/community/provider.test.tsx
  - apps/web/components/community/community.test.tsx
---

# Stop the recurring CI flakes: image pulls, keep-alive resets, offline catch-up, disposed route bodies, success artifacts

## Why

On 2026-09-15 the owner asked for CI to be fixed. `main` was green, but `#351 CI is red on main`
had been open since 2026-09-08 with twelve comments, and open PRs kept going red for reasons
their diffs could not explain.

A multi-agent triage read every failed job in the last 60 failed workflow runs (2026-09-13 to
2026-09-15): 98 failed jobs, which clustered into 18 distinct problems. 13 were branch bugs a
later push or merge had already fixed, or flakes already fixed on main (#493 for the dialog and
focus races, #468 for the new-trip draft). Five were still live. Each root cause and fix below
was checked by two adversarial verifiers, and all were judged sound.

1. **Image pulls had no retry (7 occurrences, 5 branches).** `docker run` pulls a missing image
   once. The requests it failed on were the registry ping, the token, the manifest and its
   config: quay.io 502/504/reset for MinIO, and auth.docker.io reset/timeout for mailpit and
   nginx. dockerd's `max-download-attempts` does not cover these, so a single failed request
   turned `api`, `containers`, `full-stack-smoke` or `discovery-browser` red with exit 125. A
   sibling job pulled the same image within seconds each time.
2. **Community e2e `read ECONNRESET` (4 in this window, recurring since 2026-09-08).**
   Playwright's APIRequestContext reuses keep-alive sockets with no client idle timeout and
   `maxRetries` 0. CI's `next start` ran with Node's default idle close of 5 s + 1 s, and
   `registerAndVerify` reuses its context after a browser-only gap of about 6 s at
   `community.spec.ts:34`. That is the same race production already fixed for nginx→Next with
   `KEEP_ALIVE_TIMEOUT=65000`.
3. **Community offline redelivery timeout (2 occurrences).** A real product bug.
   `context.setOffline(true)` leaves an open EventSource connected, so events delivered while
   offline trigger refreshes that fail. Nothing refreshed again once the browser was back
   online. The reader caught up only if the author's read receipt happened to arrive after
   `setOffline(false)`. Otherwise `community.spec.ts:155` timed out.
4. **`site-pages.spec.ts:239` "Response has been disposed" (blocked #517).** The read-only admin
   test can finish while the `/auth/me` route handler is between `route.fetch()` and
   `response.json()`. Context teardown clears the fetched body, and the handler's error fails
   the test. The test trace showed `json()` running 4 ms after "Close context".
5. **`#512` `app/llms.txt/route.test.ts`.** A combination bug, not a flake: #511 added a
   `server-only` import to `app/sitemap.ts`, which the test loads. It was fixed on #512's own
   branch (`b9e33349`) with the same mock `app/sitemap.test.ts` uses, so it is not in this change.

Found separately on 2026-09-14: 122.7 GB of unexpired artifacts. PR #497's required `web` job
went red on `Failed to FinalizeArtifact: ... (403) Forbidden` after every test passed. Five
workflows uploaded `apps/web/test-results` with `if: always()`, about 280 MB per passing commit.

## Definition of done

- [x] Container images used by `docker run` in CI are pulled with bounded retries, and a refusal
      (`denied`, `unauthorized`, `manifest unknown`, `not found`) still fails fast.
- [x] The CI web server keeps idle connections as long as production does (65 s), so a reused
      Playwright socket is not closed under it.
- [x] A community page catches up when the browser comes back online, with a unit test that
      fails without the fix.
- [x] The read-only site-pages test cannot end while its session route handler is mid-flight.
- [x] Browser test results upload only when a job failed or timed out.
- [ ] Ten consecutive `full-stack-smoke` runs after merge with no `read ECONNRESET` and no
      `community.spec.ts:155` timeout (carried over from the two community tasks this closes).
- [ ] No `exit code 125` image-pull failure in CI for a week after merge, other than a logged
      refusal.

## Steps

- [x] `tools/ci/pull-images.sh`:
  - 5 attempts with a `timeout 120` each, backoff of attempt × 10 s, and fail-fast on refusals.
  - It writes output to a file, so the exit code is docker's own.
  - Worst case stays under 12 minutes, inside discovery-browser's 25-minute job timeout.
- [x] `ci.yml` (`api`, `containers`, `full-stack-smoke`) and `travel-discovery.yml`
      (`discovery-browser`):
  - each image is named once as a job env var;
  - an early "Pull container images" step pulls it;
  - every `docker run` uses `--pull=never "$VAR"`.
- [x] "Failure logs" and "Show service logs on failure" tolerate missing log files. A pull
      failure no longer adds a second, misleading red step.
- [x] `apps/web/package.json` `start` is `next start --keepAliveTimeout 65000`.
  - This covers `ci.yml`, `travel-discovery.yml`, `seo-audit.yml` and the `serveBuild` branch of
    `playwright.config.ts` in one place.
  - Production runs `node apps/web/server.js` with `KEEP_ALIVE_TIMEOUT`, never `npm start`.
- [x] `components/community/provider.tsx` adds an `online` listener that runs the existing
      `update()`, and removes it in the effect cleanup.
- [x] `provider.test.tsx` has the regression test; it fails without the listener. Its
      `afterEach` unstubs globals.
- [x] `community.test.tsx` has a `MessageCenter` recovery test: refresh fails offline, the next
      one succeeds, the log comes back with each message once.
- [x] `community.spec.ts`: the offline-step comment now says it checks online catch-up, not a
      Last-Event-ID replay.
- [x] `site-pages.spec.ts`:
  - the read-only test waits for the proxied GET `/auth/me` before asserting;
  - the dirty-draft Back test waits for `/en/my`'s session response, then the admin page's, so
    one cannot satisfy the other.
- [x] The five `apps/web/test-results` uploads use `if: failure() || cancelled()`. `cancelled()`
      keeps timed-out jobs.
- [x] `tools/ci-images.test.mjs` guards all of this:
  - pull steps, `--pull=never`, one tag per image variable;
  - start script = `KEEP_ALIVE_TIMEOUT`;
  - upload conditions;
  - the helper's behaviour against a fake `docker`: success, transient then success, refusal
    fast-fail, attempts exhausted, invalid `PULL_ATTEMPTS`.

## How to verify

```bash
npm run test:tools
cd apps/web && npx vitest run components/community/provider.test.tsx components/community/community.test.tsx
```

Then watch CI:

- a transient pull shows `::warning::docker pull … failed (attempt n/5)` followed by success,
  not exit 125;
- `full-stack-smoke` stops producing `read ECONNRESET` at `community.spec.ts:34` and timeouts at
  `:155`;
- a passing run uploads no `*-browser-results` artifact.

## Notes

- **Playwright could not run locally.** The installed browsers are build 1234, but Playwright
  1.63.0 needs 1243. The community suite also needs PostgreSQL, MinIO and Mailpit. The two
  e2e spec changes are verified in CI only.
- **`.github/workflows/ci.yml` was claimed with `--force`.** `2026-09-14-article-image-ci`
  (codex-image-ci) still holds it in `review`, but its PR #470 merged on 2026-09-14T01:55Z.
- **Deliberately not done, each worth its own task if it recurs:**
  - pin `axllent/mailpit:latest`, or move it to `ghcr.io/axllent/mailpit`;
  - give CI's uvicorn `--timeout-keep-alive`; no reset has been seen on that hop;
  - add an `onerror` handler to the community EventSource; a non-200 reconnect closes it for
    good;
  - have `useResource` keep its last good data when a refresh fails;
  - make llms.txt's `openPaths` respect the `community`/`hub` flags the way `sitemap.ts` does
    (#512);
  - move `SITEMAP_ROUTES` into a module with no server imports.
- **Refuted during triage:** nothing in the five problems above was refuted. The 13 closed
  problems are listed in the triage output that produced this task: 60 runs, 98 jobs.
