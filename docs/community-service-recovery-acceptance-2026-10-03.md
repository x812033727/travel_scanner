# Community isolated service recovery — 2026-10-03

Status: implementation prepared; real-service execution is pending the same-PR
`full-stack-smoke` CI job. Collection, lint or mock-unit results are not service
acceptance. This work does not activate community, set a production capacity SLO,
change the production SMTP configuration or complete the foundation ticket.

## Execution boundary

`tests/test_community_service_recovery.py` requires both
`COMMUNITY_SERVICE_RECOVERY_E2E=1` and `RUN_INTEGRATION_TESTS=1`. Execution requires Linux `/proc`; other platforms refuse before starting services.
It starts the actual
FastAPI application, ordinary RQ worker and community sweeper in fresh processes.
It migrates a randomly named private PostgreSQL database, claims an initially empty
nonzero Redis logical database, creates a unique private MinIO bucket and uses
unique synthetic recipients in the existing local Mailpit service. All backing
service addresses must be literal loopback. It does not stop shared CI containers,
flush their Redis server or modify the browser suite's database/settings.

A clean child environment and an isolated working directory exclude repository
`.env` files and ambient provider credentials. The translation fixture answers
Gemini HTTP requests with a synthetic key; the application still runs the actual
`GeminiStructuredProvider` HTTP request, envelope decoder and structured parser.
There is no application dependency override, monkeypatched provider, disabled
production authentication guard or paid upstream call.

TCP proxies affect only the fixture's Redis, SMTP and S3 connections. The storage
container and its existing objects remain alive during S3 failure. Teardown stops
only processes in sessions created by this fixture (including RQ work horses that
change process groups), rechecks each PID start time, verifies no live member remains, closes its proxy connections
and removes only its own database, bucket and claimed Redis data. It never launches
a browser or contacts production.

## Six acceptance contracts

| Scenario | Required observable proof |
| --- | --- |
| Worker stopped and restarted | A real verification request commits an encrypted pending PostgreSQL job and RQ wakeup while worker/sweeper are stopped. Restart delivers actual Mailpit mail, clears the payload and allows token consumption once; replay is rejected. |
| Redis outage and lost wakeup | An established SSE stream becomes unavailable; a fresh authenticated mutation fails closed without a database message. After restoration, durable message/event cursors and idempotent replay do not duplicate data. The fixture discards only its own transient `rq:queue:community` wakeup and proves the real sweeper delivers the retained database mail job. |
| SMTP outage | A real reset request fails its first SMTP attempt, retains encrypted payload and schedules the unmodified 120-second first backoff. With the actual 60-second sweep, Mailpit receives the reset and its token works. A separate explicitly expired synthetic job completes without mail and is never counted as delivery. |
| S3 outage | A real signed upload preserves quarantine data when completion returns 503; restoring the proxy processes both actual image variants. Account deletion revokes access immediately, remains retryable while S3 is unavailable and removes the owned objects/PII after restoration. |
| Translation failure, cache and budget | Controlled HTTP 503 and malformed structured output return 503, retain the original and reserved provider budget, and create no cache/member charge. Success is cached; repeated reads make no upstream call. The real admin budget setting rejects a new locale before HTTP at 429 and recovers after its limit is raised. |
| Translation during revision | A barrier holds the real provider HTTP response while the real author/admin endpoints publish a new revision. Releasing the stale response returns 409 and creates no stale cache/member charge; retry caches only the new fingerprint. |

The 210-second recovery wait covers the product's 120-second first retry plus
60-second sweep and bounded scheduling margin. It is a test deadline, not a
production SLO. The fixture never edits `available_at` to speed up a retry.
The one expired-job fixture deliberately edits only `created_at` to test the
separate skip branch. SMTP has at-least-once delivery: a crash after acceptance by
SMTP but before database commit can redeliver; this suite does not claim otherwise.

## Evidence and remaining gate

Local preparation on Python 3.13.15 passed Ruff, Ruff format checks, AST parsing
and scoped mypy for the three new Python files. Guarded `pytest --collect-only`
found the exact six scenarios without running fixtures or test bodies. Both
opt-in variables were absent, repository environment-file loading was disabled,
and network access was denied (only the standard library's internal socket-pair
mechanism was permitted). No service was started. Independent source review also
passed; these results establish a reviewable candidate, not runtime acceptance.

The CI step prints a sanitized receipt with scenario checks, source hashes and the
CI SHA. It prints no mail links, cookies, access tokens, raw provider input or child
environment. A valid acceptance record must include the immutable run/job URL,
exact tested SHA, six passed cases, no skips, and successful owned-resource cleanup.
No such run is claimed in this prepared document; attach the actual result after CI.

The five-locale real browser matrix is separately tracked in
[the local acceptance record](community-local-acceptance-2026-09-29.md).

## Capacity proposal requiring owner review

No existing operational capacity/SLO threshold was found. Current settings are
product limits, not load acceptance: 50 uploads/member/day, 10 posts/member/day,
30 interactions/member/minute and 100,000 translation characters/month by default;
the job drain processes up to 25 due jobs and the sweeper runs every 60 seconds.

A concrete proposed later run is 10 synthetic active members, 100 approved posts,
5 requests/second for 5 minutes (90% reads, 10% writes), plus 60 pending mail jobs
from distinct fixture accounts. Suggested bounds: read p95 at most 1 second, write
p95 at most 2 seconds (excluding intentionally held translation), zero lost accepted
writes or logical duplicates, no unexpected 5xx outside deliberate outages, a clean
60-job backlog within 180 seconds and post-recovery latency at most twice baseline.
The distinct accounts preserve the real three-mails-per-account/hour limits.

These numbers remain a proposal. Owner approval and a real load run are still
unchecked; passing the six recovery scenarios does not complete capacity or public
activation acceptance.
