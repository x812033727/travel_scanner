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
This prepared version's first browser result is recorded below; it did not pass.

### First 30-case execution and administrator locale correction

At exact head `641e2576a2212550db384cfe5b9d3a3dc98b0b8f`,
[full-stack job 111212893808](https://github.com/x812033727/travel_scanner/actions/runs/37126555983/job/111212893808)
ran all 30 cases with two workers: **12 passed, 18 failed, zero skipped**.
All ten account-safety cases and both Traditional Chinese pet journeys passed.
This failed matrix is distinct from that job's other successful service and
administrator steps; later assertions in interrupted journeys remain unexecuted.

Ten publication journeys failed at the report dialog's backward Tab boundary:
the close button was focused, but Shift+Tab did not focus the enabled Submit
button. The native dialog had no explicit boundary handler. The trace does not
capture `document.activeElement`, so it does not prove a specific final focus
destination. This is tracked as a shared-dialog product correction. The matrix
keeps its original keyboard expectations; entering a report reason, changing
the expected focus, skipping or extending the timeout would not resolve it.

The other eight failures were the non-Traditional-Chinese pet administrator
fixtures. Each trace shows the requested locale changing to
`/zh-TW/admin/pet-friendly`: the shared administrator's saved locale legitimately
overrode the initial route, while the test still searched for its requested
language's review button. The exact pending candidate was present in the
Traditional Chinese administration page.

Only that isolated administrator browser context now records an explicit
session locale choice before navigation, using the same
`travel-locale-picked=1` session-storage marker as the public language picker.
The script is restricted to the loopback site origin. It does not change
authentication or PATCH the shared administrator's preference, which would race
parallel cases. Before using translated controls, the test additionally asserts
the exact administrator URL and document language. Removing these additions
restores every byte of the previous spec, preserving all 37 original non-UI
assertions, the keyboard checks, quota use and timeout settings.

The private diagnosis is `community-real-matrix-20261003/ci-641e-diagnosis.json`,
SHA-256 `f7cff9e87e7c38fe1c128212592d15daed375d21561e48e56dc0b62dbb275126`.
It binds all 18 failure traces and the unchanged source at the failing head.
One artifact download was shared with the existing job log; no production,
provider or additional login was used for diagnosis. The corrected matrix still
requires a fresh isolated-stack execution, including the shared-dialog fix;
the used stack must not be reused to evade or exhaust its reset quota.

For the corrected spec SHA-256
`f5c0fd98be387ed7bb49018d9d022cd8977b5e39fb4932b2beddc014c1a3bc06`,
scoped ESLint passed (exit 0) and Playwright discovery passed (exit 0, 30 cases)
on captured bundled Node v24.21.0. The spec hash was identical before and after
both commands; scoped `git diff --check` passed. Actual argv, runtime, times,
logs and the byte-preservation proof are recorded privately in
`community-real-matrix-20261003/locale-fix-checks.json`. The updated full web
typecheck subsequently passed on 2026-10-03 at 14:02:37 UTC, exit 0, with all
three UI/test/spec hashes unchanged. The owned TypeScript compiler used bundled
primary Node v24.19.0; the npm command used the installed npm shim. Private
receipt `task-continuation-20261003/ui-locale-typecheck-20261003T140129996Z.json`
has SHA-256 `19246e133ad7e4cbbff58efb52ace2ecf3cabed31ceb026163660ce9ad8d8a5e`.
These checks do not execute the browser; the corrected exact-head CI is pending.

### Second 30-case execution and Japanese composer locator

At exact head `70174ca194dc386ead9c02a1e70cc1d0aed7645a`,
[full-stack job 111219014934](https://github.com/x812033727/travel_scanner/actions/runs/37128624919/job/111219014934)
checked out `a52226de3d79d89e817cecd10ed05f237ecd1916` and ran the community
matrix: **28 passed, 2 failed, zero skipped**, in 6.6 minutes with two workers.
The initial report-dialog keyboard failures and administrator-locale failures
did not recur. The two failures are the Japanese publication/message journey
on desktop and Pixel 7; this is still a failed matrix, not whole acceptance.

The log lists four exact matches for `getByLabel("メッセージ")`: the tab list,
tab panel, message log and composer textarea. Japanese uses the same text for
the singular and plural message labels. Both composer references now use the
`textbox` role with the exact catalog label, for filling and theme checks. Only
these two locator expressions change; reversing them restores every byte of
the `70174ca` spec. All 37 original non-UI assertions, keyboard checks, isolated
administrator locale selection, authentication, quotas and timeouts remain.
The completed job log fully identifies this mismatch; no additional browser
artifact download or service execution was needed for diagnosis.

In the same job, the six real-service recovery scenarios passed with zero
failures or skips in 392.33 seconds. Its emitted receipt binds the new runtime
SHA-256 `625c01c131a9b54265fc7c8141f4236ddaafdda72f4d07f89bdcea7eb08d093e`
to the actual checkout and confirms owned fixture processes stopped while
shared services were preserved; later application/container cleanup steps also
succeeded. Operational capacity remains explicitly unaccepted. This separate
recovery success does not turn the two browser failures into a pass.

Canonical private evidence:
`community-real-matrix-20261003/ci-70174ca/canonical-receipt.json`, SHA-256
`90073327ab7d271fa4cba80f01f65bf89ca160abe70a18a4d8b48c5001535a60`.
The actual checkout's Dialog, Dialog test and community spec bytes match the PR
head exactly. The first 18-failure receipt and this two-failure receipt are both
preserved. Another fresh isolated-stack run is required for the corrected spec.

For corrected spec SHA-256
`21da9cdb3caad36061782af41669a3fc445dae952bbf04e432cf5ce8fe3ced5c`,
scoped ESLint and Playwright discovery both returned exit 0 on captured bundled
Node v24.21.0; discovery found exactly 30 cases. The source hash was unchanged
before and after both checks. Private
`community-real-matrix-20261003/ci-70174ca/ja-fix-checks.json` records the actual
argv, times, log hashes and exact two-substitution byte-preservation proof.
These checks do not execute the browser or supersede the 28-pass/two-failure
result; full TypeScript and fresh exact-head browser verification remain pending.

### Final corrected source acceptance

At PR head `ba5c6ae01df9eeffd13fc74233f7d37db0553c59`, all 23 checks completed
successfully. [Full-stack job 111223852163](https://github.com/x812033727/travel_scanner/actions/runs/37130278372/job/111223852163)
checked out `07c25196ba1c0901aad6600a5789584090496642` and executed all 30
community journeys: **30 passed, zero failed, zero skipped**, in 5.5 minutes
with two workers. This covers five locales, desktop and Pixel 7, the existing
permissions and account-safety assertions, both themes, dialog keyboard
boundaries, the isolated administrator locale and the Japanese composer.
The final spec SHA-256 is
`21da9cdb3caad36061782af41669a3fc445dae952bbf04e432cf5ce8fe3ced5c`.
The Dialog and its unit-test bytes also match their independently reviewed
`edd54a41...` and `d7fb81c9...` hashes in the PR head and actual checkout.

The same job passed all six real-service recovery scenarios in 387.60 seconds,
with zero failures or skips. Its receipt binds corrected runtime SHA-256
`625c01c131a9b54265fc7c8141f4236ddaafdda72f4d07f89bdcea7eb08d093e`.
Owned processes stopped, shared services were preserved, and the application
and container cleanup steps succeeded. Capacity acceptance remains false.

[Web checks](https://github.com/x812033727/travel_scanner/actions/runs/37130278372/job/111223852184)
passed complete ESLint, five-language i18n, web TypeScript and task validation.
The complete tools suite selected 1,494 cases: 1,493 passed, zero failed and one
optional browser-render case skipped. Actual Node was v24.21.0. Private web
completion receipt SHA-256:
`3102632324586a2d98d3cf4760c68d6fb04d880df617f1d33d7d7ffad0183f59`.

Canonical private full-stack receipt:
`community-real-matrix-20261003/ci-ba5c6ae/canonical-receipt.json`, SHA-256
`a33b0c59e320d8a65defe2ed7519ddaccf1627e68becc6041bf5352044e8eba7`.
Complete 23-check snapshot SHA-256:
`1a94a1b431240bd2e2a7e9623afe53cbbdad3295708d1e78e86f35f236f5f99d`.
The earlier failed-head receipts remain preserved. These successful source
checks complete the community web and dialog tickets; the foundation ticket
stays in review for owner/capacity acceptance. They do not authorize production
activation, deployment, publication, paid generation or uploading. A later
metadata-only commit must record its own CI result separately.
