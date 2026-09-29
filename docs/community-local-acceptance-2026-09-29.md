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
