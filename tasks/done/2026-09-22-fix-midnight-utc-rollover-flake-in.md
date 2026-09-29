---
id: 2026-09-22-fix-midnight-utc-rollover-flake-in
title: Fix midnight UTC rollover flake in test_ai_trip_parser_llm
status: done
priority: P2
area: api
owner: codex-test-isolation
claimed_at: 2026-09-29T06:43:09Z
created_at: 2026-09-22T00:30:56Z
completed_at: 2026-09-29T06:51:42Z
branch: codex/test-isolation-fixes
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

- [x] The test passes regardless of when it runs, including across a UTC day
      boundary, and does not depend on the wall clock agreeing between import
      time and call time.
- [x] The test still proves the parser puts the current date into the prompt —
      a parser that omitted the date, or sent a stale one, still fails.

## Steps

- [x] Freeze the date for the test instead of reading the clock twice: either
      inject/patch the clock the parser uses so both sides see one fixed date,
      or read the expected date from the same source the parser reads at call
      time rather than at module import.
- [x] Check the other module-level date captures in the same file for the same
      pattern. Note that the `date.today() + timedelta(...)` offsets elsewhere
      in `apps/api/tests` are not affected — they never compare a captured
      literal against a freshly computed one.

## How to verify

From `apps/api`, run
`.venv/Scripts/python.exe -m pytest tests/test_ai_trip_parser_llm.py`.
Then simulate a next-day parser wall clock while keeping the suite's captured
date fixed: the existing test must pass. Supplying a stale or omitted prompt
date must still fail at the current-date assertion. As a negative control,
removing that assertion in memory makes the omitted-date mutation pass; a
verification harness must reject that unexpected pass when testing the real
suite's protection.

## Notes

Failing job for reference:
`https://github.com/x812033727/travel_scanner/actions/runs/35669929503/job/106563887880`.

The fetched log needs `gh api --allow-escape-sequences` to read; plain
`gh run view --log-failed` refuses it and `--allow-escape-sequences` is not a
flag on `gh run view`.

### 2026-09-29 verification of the already-merged fix

PR [#839](https://github.com/x812033727/travel_scanner/pull/839) already fixed this
on 2026-09-27 in commit `07d33b61eb43ebfa4a9599f1d7f5a8555c36655f`.
The autouse `_parser_today_is_the_suites_today` fixture pins the parser's `_today`
to the test module's captured `TODAY`. `DEPARTURE`, `RETURNING` and
`DEPARTURE_MONTH` all derive from that same date; there is no second independent
module-level date capture. The current-date assertion remains in the original
provider/prompt test. Fresh main `c1fe22fca190c219dcf2ffd20dea466a99dfdd81`
still contains that fix. No additional parser or test-file change was needed.

Independent local verification used the worktree API venv and the original
`tests/test_ai_trip_parser_llm.py`: **38 passed, 0 skipped, exit 0**.
An external pytest plugin then ran the original provider/prompt test in isolated
processes, with suite date `2040-12-31` and parser wall clock
`2041-01-01T00:05:00+00:00`:

- Existing fixture retained: **1 passed, exit 0**, despite the UTC year boundary.
- Restoring the unpinned parser clock in memory: **1 expected failure, exit 1**
  at the retained current-date assertion.
- Supplying the previous day's date in the prompt: **1 expected failure, exit 1**
  at the same assertion.
- Omitting the date from the prompt: **1 expected failure, exit 1** at the same
  assertion.
- Omitting the prompt date and removing only that assertion in memory:
  **1 passed, exit 0**. This negative control demonstrates why the assertion must
  remain; the probe runner rejects an unexpected pass in either prompt mutation.

All six probe outcomes matched their expected result. `probe-result.json`
SHA256: `f675e37bab21d10af7d7aba6c453dc8c547a4a13444f0870fcb827c44d0319ca`.
It binds helper and log hashes and verifies the repository parser and test bytes
were unchanged before and after execution. The fixture transports are mocked;
no production access, paid provider call or database service was used. The
deliberate failures are mutation controls, not failing repository checks.

The collision audit found no active claim or open PR touching this file and no
modified copy in the normal local worktrees. Historical inaccessible/sparse
localization checkouts were left untouched. This update reconciles a stale task
with an existing merged fix and verified regression coverage.
