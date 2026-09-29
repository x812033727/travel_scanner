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

## Still required

- Real-service translation provider failure and changed-original handling.
- Worker restart, durable notifications/job recovery, Redis/SMTP/S3 outages and
  a defined operational capacity/load acceptance target.
- Full real-service five-locale light/dark journeys for publishing, moderation,
  collections, messaging, pet rules, account recovery and deletion.
- Separate owner approval and current production verification before launch,
  including policies/contact details, provider setup, budget and moderation staff.
