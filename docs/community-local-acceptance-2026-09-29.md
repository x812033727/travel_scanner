# Local community acceptance, 2026-09-29

This pass uses the current main implementation at `c1da5fad` plus a new synthetic
browser suite. It neither contacts production nor activates community services.
PR #340 and the account-safety follow-up #343 are already merged. Their dated
real-service records remain historical evidence; they are not current load tests.

## API contracts

`apps/api/.venv/Scripts/python.exe -m pytest tests/test_hotspot_discovery.py
tests/test_community_foundation.py -q` from `apps/api` completed with **52 passed,
8 skipped**, in 213.84 seconds. The eight skips require PostgreSQL or private S3.
The local machine has no Docker command and no listening PostgreSQL, Redis,
MinIO or Mailpit companion services. No integration skip is counted as a pass.

The community contracts cover mutual messages and block scope, account-token
replay/erasure, translation caching/edit invalidation/budget, conservative pet
eligibility and durable-job erasure. This does not exercise actual Redis outage,
process restart, SMTP delivery, S3 failure or operational capacity.

## Browser UI matrix

`apps/web/e2e/community-ui.spec.ts` declares 20 cases: five locales, light/dark
appearance, and desktop/Pixel 7. It is included in the required Web CI job. All
responses and identities are visibly synthetic; external browser requests and
unexpected writes are blocked and asserted absent.

Each case exercises the rendered feed and post, a translation 503 retaining the
original, retry success, a newer published revision returned by a normal reaction
refresh, removal of the old translation, translation of the new revision, and
return to the original. It also checks report-dialog Escape/focus restoration,
viewport overflow, uncaught page errors and a screenshot.

This suite is UI-contract evidence only. It supplements `community.spec.ts`; it
does not replace that suite's real PostgreSQL/Redis/MinIO/Mailpit/worker journeys.
Local execution results:

- Scoped ESLint passed; Playwright `--list` discovers all 20 cases.
- Existing community component tests passed: 10 files, 52 tests, 147.69 seconds.
- Next production build and its TypeScript check passed, generating 348 pages.
- **The 20 browser cases have not run locally.** Automatic approval review
  rejected the command that starts Next on `127.0.0.1:3317` with
  `rejected: blocked by policy`; no more specific reason was returned. The
  command used `API_INTERNAL_URL=http://127.0.0.1:8000` and the completed local
  build. No equivalent launcher was used to bypass the rejection.
- CUA inventory returned no browsers; creating an IAB tab returned
  `Browser is not available: iab`, and creating a Chrome tab timed out. Thus no
  built-in-browser inspection or new browser screenshot is claimed.

The existing required Web workflow will execute the new matrix against its
normal isolated server. Exact-head CI results are required before these browser
cases can be described as passed.

### First CI execution and locator correction

The first required Web job at head `254c94e24aefa01123b5c4b77cedb7a981c01f9b`
actually ran the matrix: [job 109225869105](https://github.com/x812033727/travel_scanner/actions/runs/36511969464/job/109225869105)
finished with 20 failures, 523 other passes and 9 skips. Although the overall run
was subsequently cancelled, this Web job's browser step had already failed;
it is neither a passed matrix nor merely an unexecuted cancelled job.

All 20 new failures had the same strict-locator cause at the translation error
assertion: `getByRole("alert")` matched both the localized error paragraph and
Next's `__next-route-announcer__`. The trace text shows the expected translation
error was present. The test now filters the alert by the exact localized error
text, still asserts the complete text, and checks that same alert disappears
after retry. The later global alert-count assertion needed the same correction,
because the route announcer persists after a successful translation. No product
code was changed and no assertion was removed. A fresh CI head must execute all
20 cases after this correction before this matrix can be called passed.

After the locator correction, scoped ESLint, Playwright discovery (20 cases),
and `git diff --check` each completed with exit 0. These checks do not execute
the browser matrix; its fresh-head CI result is still required.

## Immutable CI receipt: `eefce5fd`

On 2026-09-29, [CI run 36513935070](https://github.com/x812033727/travel_scanner/actions/runs/36513935070)
completed successfully for exact head
`eefce5fd0ef043528bc0eb90ef0fe3abd34cc384`. All four required jobs passed:

| Job | Evidence |
| --- | --- |
| [web](https://github.com/x812033727/travel_scanner/actions/runs/36513935070/job/109232014172) | Lint, i18n, task checks, typecheck and build passed; 333 component files / 3,551 tests and 673 tool tests passed. The isolated browser command explicitly included `community-ui.spec.ts`: 543 passed, 9 skipped, 0 failed in 7.2 minutes, completed at 03:01:19 UTC. |
| [api](https://github.com/x812033727/travel_scanner/actions/runs/36513935070/job/109232014247) | Ruff, both mypy checks and migration checks passed; full pytest: 5,548 passed, 16 skipped, 10 warnings in 1,367.19 seconds. Job completed at 03:08:47 UTC. |
| [containers](https://github.com/x812033727/travel_scanner/actions/runs/36513935070/job/109232014325) | Container builds, production Compose and reverse-proxy/image rate-limit checks passed. |
| [full-stack-smoke](https://github.com/x812033727/travel_scanner/actions/runs/36513935070/job/109232014021) | Existing real-service community suite: 6 passed. Other journeys: 8 passed; isolated admin: 2 passed; admin operations: 6 passed / 6 skipped. |

The new community UI matrix's **20 cases passed**: five locales × two color
schemes × desktop/Pixel 7. The CI log uses a dot reporter and only prints the
combined browser total, not individual case names. The 20-case count comes from
Playwright discovery and the unchanged spec's unconditional test definitions;
the spec has no skipped cases and was included in the successful full command.
This validates translation failure/retry, changed-original recovery, original
text restoration, report-dialog keyboard/focus behavior and viewport overflow
against the explicit synthetic fixture. It does not turn those scenarios into
real-provider, outage or load tests.

At this head, all five additional checks also passed: release-safety,
food-map-reservations, planner-browser, discovery-browser and lighthouse.
This receipt is bound to `eefce5fd`; a later merge of the story worker or any
other new commit has a different head and needs its own CI result. No merge,
deployment, production browser visit or live community acceptance is implied.

## Still required

- Real-service translation provider failure and changed-original handling.
- Worker restart, durable notifications/job recovery, Redis/SMTP/S3 outages and
  a defined operational capacity/load acceptance target.
- Full real-service five-locale light/dark journeys for publishing, moderation,
  collections, messaging, pet rules, account recovery and deletion.
- Separate owner approval and current production verification before launch,
  including policies/contact details, provider setup, budget and moderation staff.

## Real-service matrix prepared, 2026-10-03

The continuation at main `5f1cec5302511ac0c6f7eddffaf5f988a8c95a7d`
expands the existing `community.spec.ts` journeys to **30 cases**: three
journeys × five locales (`zh-TW`, `zh-CN`, `en`, `ja`, `ko`) × desktop Chromium
and Pixel 7. This is source preparation, not a passed browser receipt. The
current full-stack CI workflow still selects this spec; no workflow, application,
catalog or production setting is changed by this continuation.

| Journey, each locale and viewport | Real-service checks retained and added |
| --- | --- |
| Publishing, private images, collections and messages | Ordinary verified members; an unpublished post/image stays 404; moderation makes the reviewed post visible; public itinerary never contains the private trip note; fork is 201 and repeated reads have no duplicate system roles. A collection created through the UI contains the exact post and another member receives 404. Mutual-follow permission, offline catch-up without reload, idempotent delivery, unfollow 403 and block 404 retain their original assertions. |
| Reviewed pet rules and trip requirements | Pending places remain 404; an actual administrator reviews the source; unknown species are excluded until explicitly included. A conflicting trip addition needs confirmation, adds once and preserves private notes. A traveller report remains unpublished until review, flags uncertainty without changing the underlying policies, and the post's association resolves to the exact pet place. |
| SMTP recovery and deletion | Each member receives actual isolated SMTP verification/reset/deletion links in their locale. Reset revokes old sessions, rejects the old password and token replay; deletion revokes sessions and hides the public identity. Existing 401/400/404 assertions remain. |

All ordinary enrollments also assert denial of the admin settings endpoint.
Selectors use the actual five-language catalogs and the planner's existing copy;
registration stores the selected locale, and each mail confirmation path is
checked against it. No synthetic identity or intercepted API response replaces
these real-service journeys.

Both light and dark themes are checked **within** each of the 30 cases at key
rendered UI checkpoints, using the normal system-theme preference. Assertions
check the actual `data-theme`, visible/enabled controls and horizontal overflow.
Post report dialogs exercise Enter, backward/forward Tab boundaries, Escape and
focus return in both themes; pet report dialogs also check keyboard opening and
Escape/focus restoration. Account reset confirmation controls are checked in
both themes. This is not 60 separately repeated SMTP journeys or a claim that
every intermediate screen has an independent visual review.

The worker fixture signs into the existing disposable CI administrator with a
real API request. Only that administrator's context is reused; the pet admin
browser receives its real cookie storage state. All ordinary members and stale
sessions remain separate. Setup first requires a loopback site origin and
explicit `COMMUNITY_E2E=1`; translation is disabled in this isolated community
setup. No translation endpoint, paid provider, production login or uploader is
used. The older 20-case synthetic translation matrix remains separate; real
translation failures, revisions and operational outages remain foundation gates.

### Quota and execution prerequisites

For one clean run, the community matrix creates 40 ordinary accounts and makes
50 member login attempts plus one administrator login per Playwright worker
(normally two workers for the two projects). The full-stack suite before it
adds eight registrations; later admin acceptance adds eight registrations and
16 logins (including the deliberately rejected suspended-member login). Thus
the shared-stack totals are **56 registrations and normally 68 login attempts**,
below the CI limits of 100/hour and 100/15 minutes. No
production limit is raised. Without admin-session reuse the login total would
be 96 before failures or retries.

The ten recovery journeys use **exactly ten** forgot-password requests, matching
the independent hard reset-IP limit of ten/hour. The current Playwright config
has no retries. A new full acceptance run needs a fresh disposable stack/rate
namespace; do not rerun it against the same recently consumed Redis counters or
alter limits to hide a 429. Real verification/deletion limits are per member,
and each new member uses each relevant operation once.

Execution requires the existing isolated PostgreSQL, Redis, private MinIO,
Mailpit, real API, RQ worker and built Web application, including the existing
fixture administrator and environment used by the full-stack CI job. Discovery,
lint and TypeScript checks do not start these services or validate the 30
journeys. A fresh exact-head execution receipt, screenshots/traces and failure
review are still required before checking off the real-service matrix step.

Preparation checks completed with bundled Node **v24.21.0**: scoped ESLint
returned exit 0, and Playwright `--list` returned exit 0 with exactly 30 cases
(15 per project). Neither command launches the companion stack or executes the
browser cases. Independent source review passed at spec SHA-256
`a2bfcf534bebe1a9e18e19c2eaa13fe713792fea2d5488fdcc9631c656af00fb`:
all 37 original non-UI assertions are preserved and all 77 referenced copy keys
exist in the five catalogs. The private independent JSON receipt has SHA-256
`0f4829f87bfef6ac12bc08c00d7d626b963398307d8252faabcd243b08ed6ba7`.
The complete web TypeScript check also passed (exit 0) on actual primary-runtime
Node v24.19.0, with the spec hash identical before and after the check. Its private
receipt SHA-256 is `4e8c93f0beb631c91e5d373ba36b86370f8e63094a3886650655ce05dfb405de`.
The 30-case browser result remains pending.
