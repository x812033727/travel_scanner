---
id: 2026-09-22-fix-midnight-utc-rollover-flake-in
title: Fix midnight UTC rollover flake in test_ai_trip_parser_llm
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-22T00:30:56Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/tests/test_ai_trip_parser_llm.py
---

# Fix midnight UTC rollover flake in test_ai_trip_parser_llm

## Why

`test_llm_parse_reports_the_provider_and_resolves_the_catalog` fails whenever a
CI run crosses midnight UTC. The test captures the date once at import time
(`TODAY = datetime.now(UTC).date()`, line 29) and then asserts that string
appears in the prompt the parser builds, but the parser computes the date again
when it is called. A run that starts on one UTC day and reaches this test on the
next compares two different dates and fails.

This is not theoretical. The `api` job on PR #633 (dependabot uv minor-and-patch
bump) failed exactly this way: the run started 2026-09-21T23:58:20Z and the
assertion fired at 2026-09-22T00:16:41Z with
`assert '2026-09-21' in '...'`. Nothing in that PR touches the parser — it only
bumps boto3, greenlet, sqlalchemy and ruff in `apps/api/uv.lock`. Re-running the
job cleared it. Every long `api` job that straddles 00:00 UTC is a candidate, so
the failure looks like a real regression to whoever is on the PR and costs a
diagnosis each time.

The assertion itself is worth keeping: the comment above it explains that
without today's date in the prompt the model answers with its training-era year.
The fix is to make the date deterministic, not to drop the check.

## Definition of done

- [ ] The test passes regardless of when it runs, including across a UTC day
      boundary, and does not depend on the wall clock agreeing between import
      time and call time.
- [ ] The test still proves the parser puts the current date into the prompt —
      a parser that omitted the date, or sent a stale one, still fails.

## Steps

- [ ] Freeze the date for the test instead of reading the clock twice: either
      inject/patch the clock the parser uses so both sides see one fixed date,
      or read the expected date from the same source the parser reads at call
      time rather than at module import.
- [ ] Check the other module-level date captures in the same file for the same
      pattern. Note that the `date.today() + timedelta(...)` offsets elsewhere
      in `apps/api/tests` are not affected — they never compare a captured
      literal against a freshly computed one.

## How to verify

`apps/api/.venv/Scripts/python.exe -m pytest tests/test_ai_trip_parser_llm.py`
from `apps/api`, plus a run with the clock (or the patched clock) set so the
captured date and the call-time date differ — that run must still pass with the
real fix and must fail if the assertion is simply removed.

## Notes

Failing job for reference:
`https://github.com/x812033727/travel_scanner/actions/runs/35669929503/job/106563887880`.

The fetched log needs `gh api --allow-escape-sequences` to read; plain
`gh run view --log-failed` refuses it and `--allow-escape-sequences` is not a
flag on `gh run view`.
